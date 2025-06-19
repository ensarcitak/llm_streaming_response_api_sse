import logging
from langchain_huggingface import HuggingFaceHub
from app.ai_services.provider_template import BaseLLMProvider
from typing import List
from langchain.schema import BaseMessage
from app.config.settings import settings

# Logger'ı içe aktar
from logging import Logger

# Logger'ı başlat
logger = Logger(__name__)

class HuggingFaceLLMProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "google/gemma-3-4b-it"):
        logger.logger.info(f"HuggingFaceLLMProvider is starting, model: {model_name}")
        try:
            self.model = HuggingFaceHub(
                repo_id=model_name,
                huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_TOKEN,
                model_kwargs={"temperature": 0.5, "max_length": 4096}
            )
            logger.logger.info("Model başarıyla yüklendi")
        except Exception as e:
            logger.logger.error(f"Model yüklenirken hata: {str(e)}")
            raise

    def generate_stream_response(self, messages: List[BaseMessage]):
        logger.logger.debug("Akış yanıtı üretiliyor")
        # HuggingFaceHub akış desteğini sınırlı sunar, bu yüzden metni birleştirip çağırıyoruz
        prompt = self._format_messages(messages)
        try:
            response = self.model.stream(prompt)
            for chunk in response:
                if chunk:  # Boş olmayan parçaları yield et
                    yield chunk
                    logger.logger.debug(f"Akış parçası: {chunk}")
        except Exception as e:
            logger.logger.error(f"Akış yanıtı üretilirken hata: {str(e)}")
            raise

    def generate_response(self, messages: List[BaseMessage]) -> str:
        logger.logger.debug("Normal yanıt üretiliyor")
        prompt = self._format_messages(messages)
        try:
            response = self.model(prompt)
            logger.logger.info("Yanıt başarıyla üretildi")
            return response
        except Exception as e:
            logger.logger.error(f"Yanıt üretilirken hata: {str(e)}")
            raise


    def _format_messages(self, messages: List[BaseMessage]) -> str:
        # Mesajları Hugging Face modeline uygun bir prompt haline getir
        prompt = ""
        for msg in messages:
            if msg.type == "human":
                prompt += f"User: {msg.content}\n"
            elif msg.type == "ai":
                prompt += f"Assistant: {msg.content}\n"
        logger.logger.debug(f"Formatlanmış prompt: {prompt[:100]}...")  # İlk 100 karakter
        return prompt