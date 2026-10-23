import os
from deepl import Translator
from typing import Optional


class OutputTranslator:
    def __init__(self, target_lang: str = "EN-US"):
        self.target_lang = target_lang
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        self.translator = Translator(self.auth_key)

    def translate(self, text: str) -> str:
        result = self.translator.translate_text(text, target_lang=self.target_lang)
        return result.text
