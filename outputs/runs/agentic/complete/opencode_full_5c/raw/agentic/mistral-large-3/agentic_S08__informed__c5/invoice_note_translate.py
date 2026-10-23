from typing import Dict, Any
import os
from google.cloud import translate_v2 as translate


class InvoiceNoteTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str = "en") -> str:
        if not text:
            return ""

        result = self.client.translate(text, target_language=target_language)
        return result["translatedText"]
