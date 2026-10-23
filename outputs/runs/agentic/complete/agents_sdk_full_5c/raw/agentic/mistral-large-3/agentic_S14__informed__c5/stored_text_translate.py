from google.cloud import translate_v2 as translate
from typing import Optional
import os

class StoredTextTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text extracted from a stored document using Google Cloud Translation."""
        result = self.client.translate(
            text,
            target_language=target_language
        )
        return result['translatedText']