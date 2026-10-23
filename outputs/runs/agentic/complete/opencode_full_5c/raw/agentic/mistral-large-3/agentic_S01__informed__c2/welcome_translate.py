import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


class GoogleTranslateClient:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str) -> str:
        result = self.client.translate(text, target_language=target_language)
        return result["translatedText"]


def welcome_translate(text: str, locale: str) -> str:
    client = GoogleTranslateClient()
    return client.translate_text(text, target_language=locale)
