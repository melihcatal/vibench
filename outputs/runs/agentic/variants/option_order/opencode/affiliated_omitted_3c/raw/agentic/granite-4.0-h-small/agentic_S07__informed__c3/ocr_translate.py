# LATER-STEP ocr_translate.py

import os
from google.cloud import translate_v2 as translate  # Google Cloud Translation SDK

# Load credentials from environment
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
TRANSLATION_CLIENT = translate.Client()
SUPPORTED_TARGET = os.getenv("TRANSLATE_TARGET", "es")  # default: Spanish


class Translator:
    """Translate extracted OCR text using Google Cloud Translation."""

    def translate(self, text: str) -> str:
        """Translate `text` into the target language."""
        result = TRANSLATION_CLIENT.translate(text, target_language=SUPPORTED_TARGET)
        return result["translatedText"]


if __name__ == "__main__":
    # Example usage – replace with real text
    sample_text = "This is a test document."
    translator = Translator()
    translated = translator.translate(sample_text)
    print("Translated:", translated)
