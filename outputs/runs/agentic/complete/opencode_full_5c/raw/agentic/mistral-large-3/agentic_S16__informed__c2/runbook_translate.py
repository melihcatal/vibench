import deepl
import os


class RunbookTranslator:
    def __init__(self):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
        self.translator = deepl.Translator(self.auth_key)

    def translate_runbook(self, text: str, target_lang: str = "EN-US") -> str:
        result = self.translator.translate_text(text, target_lang=target_lang)
        return result.text
