import os
from typing import Optional
from google.cloud import translate_v2 as translate


class AppealTranslator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required.")
        self.client = translate.Client()

    def translate_appeal(self, text: str, target_language: str = "en") -> str:
        result = self.client.translate(text, target_language=target_language)
        return result["translatedText"]


def translate_appeal(text: str, target_language: str = "en") -> str:
    translator = AppealTranslator()
    return translator.translate_appeal(text, target_language)