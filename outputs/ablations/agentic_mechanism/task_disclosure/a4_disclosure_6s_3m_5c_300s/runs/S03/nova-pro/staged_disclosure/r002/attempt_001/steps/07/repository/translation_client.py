import os

from deepl import Translator

class TranslationClient:
    def __init__(self):
        self.api_key = os.getenv('DEEPL_API_KEY')
        self.translator = Translator(self.api_key)

    def translate_text(self, text, target_lang):
        result = self.translator.translate_text(text, target_lang=target_lang)
        return result.text
