import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


class OcrTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str = "en") -> str:
        result = self.client.translate(text, target_language=target_language)
        return result['translatedText']