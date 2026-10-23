from google.cloud import translate_v2 as translate
import os


class ScriptTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_script(self, text: str, target_language: str) -> str:
        result = self.client.translate(text, target_language=target_language)
        return result["translatedText"]
