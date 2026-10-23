import os
from google.cloud import translate_v2 as translate
from typing import Dict


class WelcomeTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_welcome_message(self, text: str, target_language: str) -> str:
        result = self.client.translate(
            text, target_language=target_language, model="nmt"
        )
        return result["translatedText"]