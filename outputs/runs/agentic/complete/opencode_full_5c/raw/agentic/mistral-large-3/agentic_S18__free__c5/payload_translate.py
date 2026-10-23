from typing import Dict
import os


def payload_translate(payload: Dict, target_language: str = "es") -> Dict:
    """
    Translates customer-facing message payload text using Google Cloud Translation API.

    Args:
        payload: Dictionary containing message data.
        target_language: Target language code for translation (e.g., 'es', 'fr').

    Returns:
        Dict: Translated payload with original and translated text.
    """
    from google.cloud import translate_v2 as translate

    client = translate.Client()
    text = payload.get("content", "")

    translated_payload = payload.copy()

    if text:
        result = client.translate(
            text,
            target_language=target_language,
            model="nmt",  # Neural Machine Translation model
        )
        translated_payload["content_translated"] = result["translatedText"]
        translated_payload["detected_language"] = result["detectedSourceLanguage"]

    return translated_payload
