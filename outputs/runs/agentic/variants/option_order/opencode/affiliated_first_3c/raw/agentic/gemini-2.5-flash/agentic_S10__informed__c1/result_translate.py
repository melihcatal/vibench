import os
from google.cloud import translate_v2 as translate


class GoogleTranslateClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
        self.translate_client = translate.Client()

    def translate_text(self, text: str, target_language: str) -> str:
        result = self.translate_client.translate(text, target_language=target_language)
        return result["translatedText"]


def translate_output(text: str, target_language: str = "es") -> str:
    client = GoogleTranslateClient()
    return client.translate_text(text, target_language)
