# Translate Appeal Text for Review
from google.cloud import translate_v2 as translate


class AppealTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_appeal(self, text: str, target_language: str = "en") -> str:
        """Translate appeal text using Google Cloud Translation API."""
        result = self.client.translate(text, target_language=target_language)
        return result["translatedText"]