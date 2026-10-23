from google.cloud import translate_v2 as translate
from typing import Dict, Any
import os

# Initialize Google Cloud Translation client
translate_client = translate.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def welcome_translate(text: str, target_language: str) -> Dict[str, Any]:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')

    Returns:
        Dictionary containing translated text and translation metadata
    """
    if not text:
        return {"translated_text": "", "provider": "google_translate"}

    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "provider": "google_translate",
        "model": "google-cloud-translate-v2",
    }
