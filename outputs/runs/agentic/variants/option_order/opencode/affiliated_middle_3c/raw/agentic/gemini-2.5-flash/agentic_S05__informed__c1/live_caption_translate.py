import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()


class LiveCaptionTranslator:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS should be set in environment
        self.translate_client = translate.Client()

    def translate_caption(self, text, target_language="es"):
        if not text:
            return ""

        result = self.translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
