import deepl
from typing import Dict

class DashboardNoteTranslator:
    def __init__(self):
        self.auth_key = ""  # Uses DEEPL_AUTH_KEY from environment
        self.translator = deepl.Translator(self.auth_key)

    def translate_note(self, text: str, target_lang: str) -> str:
        result = self.translator.translate_text(text, target_lang=target_lang)
        return result.text

    def supported_languages(self) -> Dict[str, str]:
        languages = self.translator.get_target_languages()
        return {lang.code: lang.name for lang in languages}