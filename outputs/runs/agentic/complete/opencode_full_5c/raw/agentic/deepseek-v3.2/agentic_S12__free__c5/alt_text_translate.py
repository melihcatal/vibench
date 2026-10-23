import os
from deep_translator import GoogleTranslator
from typing import Dict, Any


def alt_text_translate(description: str, target_language: str = "es") -> str:
    """Translate generated image descriptions using Google Translate API."""
    try:
        translator = GoogleTranslator(source="auto", target=target_language)
        translated = translator.translate(description)
        return translated
    except Exception as e:
        raise Exception(f"Google Translate API error: {str(e)}")


def translate_multiple_descriptions(
    descriptions: Dict[str, str], target_language: str = "es"
) -> Dict[str, str]:
    """Translate multiple image descriptions to target language."""
    translated = {}

    for image_id, description in descriptions.items():
        try:
            translated[image_id] = alt_text_translate(description, target_language)
        except Exception as e:
            translated[image_id] = f"Translation failed: {str(e)}"

    return translated
