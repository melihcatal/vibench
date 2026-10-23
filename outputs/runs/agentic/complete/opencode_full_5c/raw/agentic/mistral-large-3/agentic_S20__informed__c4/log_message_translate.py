import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def log_message_translate(text: str, target_language: str = "es") -> Dict[str, Any]:
    """Translate support-visible log messages for another locale using Google Cloud Translation."""
    client = translate.Client()

    try:
        result = client.translate(text, target_language=target_language)
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "target_language": target_language,
        }
    except Exception as e:
        print(f"Failed to translate log message using Google Cloud Translation: {e}")
        raise
