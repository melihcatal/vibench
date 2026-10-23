import os
from google.cloud import translate_v2 as translate

class AppealTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str = "en") -> str:
        """
        Translates the given text to the target language using Google Cloud Translation API.
        """
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        # Google Cloud Translation API identifies itself through the client library and API endpoint.
        # The specific API endpoint is implicitly used by the client library, which routes to
        # 'translation.googleapis.com'.
        response = self.client.translate(text, target_language=target_language)
        return response["translatedText"]
