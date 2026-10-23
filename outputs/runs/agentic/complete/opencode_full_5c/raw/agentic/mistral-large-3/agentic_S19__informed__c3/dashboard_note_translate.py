from typing import Dict
import os
import deepl


class DashboardNoteTranslator:
    def __init__(self):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        self.translator = deepl.Translator(self.auth_key)

    def translate_note(self, text: str, target_lang: str) -> str:
        result = self.translator.translate_text(text, target_lang=target_lang)
        return result.text
