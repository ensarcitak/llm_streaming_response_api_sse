from langchain.schema import BaseMessage
from app.ai_services.provider_template import BaseLLMProvider
from app.config.settings import settings
from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
import torch

from logging import Logger

# Logger'ı başlat
logger = Logger(__name__)

class HuggingFaceLLMProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "google/gemma-3-4b-it"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=settings.HUGGINGFACE_API_TOKEN
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            token=settings.HUGGINGFACE_API_TOKEN,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
        self.model.eval()

    def generate_stream_response(self, messages: List[BaseMessage]):
        # Convert LangChain messages to a single prompt
        prompt = self._convert_messages_to_prompt(messages)
        
        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        # Set up streamer
        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True
        )
        
        # Generation kwargs
        generation_kwargs = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
            "max_new_tokens": 4096,
            "temperature": 0.5,
            "do_sample": True,
            "streamer": streamer
        }
        
        # Run generation in a separate thread to enable streaming
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        # Yield streamed tokens
        for new_text in streamer:
            if new_text:
                yield new_text

    def generate_response(self, messages: List[BaseMessage]) -> str:
        # Convert LangChain messages to a single prompt
        prompt = self._convert_messages_to_prompt(messages)
        
        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        # Generate response
        outputs = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=4096,
            temperature=0.5,
            do_sample=True
        )
        
        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove prompt from response if present
        if response.startswith(prompt):
            response = response[len(prompt):].strip()
        return response

    def get_model_name(self) -> str:
        return f"huggingface-{self.model_name.split('/')[-1]}"

    def _convert_messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        # Convert LangChain BaseMessage objects to a single string prompt
        prompt = ""
        for message in messages:
            role = message.type
            content = message.content
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        prompt += "Assistant: "  # Prepare for assistant's response
        return prompt