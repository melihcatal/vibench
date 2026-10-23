from google.cloud import translate_v2 as translate
import os


class GoogleTranslateClient:
    def __init__(self):
        self.client = translate.Client()

    def translate_runbook(self, text: str, target_language: str = "en") -> str:
        result = self.client.translate(
            text, target_language=target_language, format_="text"
        )
        return result["translatedText"]
