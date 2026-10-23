from google.cloud import translate_v2 as translate
import os
from typing import Dict, Any


class PayloadTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translates customer-facing message payload text using Google Cloud Translation.
        """
        result = self.client.translate(text, target_language=target_language)
        return result["translatedText"]


def translate_payload(text: str, target_language: str) -> str:
    """
    Translates the message payload text to the target language.
    """
    translator = PayloadTranslator()
    return translator.translate_text(text, target_language)


if __name__ == "__main__":
    message_text = "Hello, how are you?"
    translated_text = translate_payload(message_text, "es")
    print(f"Translated text: {translated_text}")
