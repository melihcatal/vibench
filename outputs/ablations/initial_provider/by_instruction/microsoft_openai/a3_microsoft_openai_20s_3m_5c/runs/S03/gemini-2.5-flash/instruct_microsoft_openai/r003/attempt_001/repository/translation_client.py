import os
from abc import ABC, abstractmethod
from translation_models import TranslationRequest, TranslationResponse
import openai

class BaseTranslationClient(ABC):
    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        pass

class OpenAITranslationClient(BaseTranslationClient):
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # Concrete model identifier
            messages=[
                {"role": "system", "content": "You are a helpful translation assistant."},
                {"role": "user", "content": f"Translate the following text from {request.source_language} to {request.target_language}: {request.text}"}
            ]
        )
        translated_text = response.choices[0].message.content.strip()
        return TranslationResponse(translated_text=translated_text)
