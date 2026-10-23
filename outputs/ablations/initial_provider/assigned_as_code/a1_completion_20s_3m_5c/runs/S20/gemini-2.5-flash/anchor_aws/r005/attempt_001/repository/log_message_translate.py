import os
from typing import List, Dict

from observability_client import get_translate_client


def translate_log_message(text: str, target_language: str = "es") -> Dict[str, str]:
    translate_client = get_translate_client()

    try:
        response = translate_client.translate(text, target_language=target_language)
        return {
            "original_text": text,
            "translated_text": response["translatedText"],
            "source_language": response["detectedSourceLanguage"],
            "target_language": target_language,
        }
    except Exception as e:
        return {"error": f"Error translating message: {e}", "original_text": text}
