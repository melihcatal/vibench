import os
from deep_translator import GoogleTranslator
from typing import Optional


def translate_image_description(description: str, target_language: str = "es") -> str:
    """Translate generated image descriptions using Google Translate API."""

    if not description or not description.strip():
        return ""

    try:
        translator = GoogleTranslator(source="auto", target=target_language)
        translated = translator.translate(description)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")

        try:
            from googletrans import Translator

            translator = Translator()
            result = translator.translate(description, dest=target_language)
            return result.text
        except Exception as e2:
            print(f"Fallback translation error: {e2}")
            return description
