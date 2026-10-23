from typing import Dict, Any
import os
from deepl import Translator


class InvoiceNoteTranslator:
    def __init__(self):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        self.translator = Translator(self.auth_key)

    def translate(self, text: str, target_lang: str = "EN") -> str:
        result = self.translator.translate_text(text, target_lang=target_lang)
        return result.text
