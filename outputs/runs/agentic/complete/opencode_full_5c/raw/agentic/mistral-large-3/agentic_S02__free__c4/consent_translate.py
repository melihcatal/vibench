from google.cloud import translate_v2 as translate
import os
from typing import Dict, Any

# Google Cloud Translation API Configuration
GOOGLE_TRANSLATE_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", "path/to/credentials.json"
)


def translate_consent_text(text: str, target_language: str) -> Dict[str, Any]:
    """Translate identity-provider consent copy using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "input_text": text,
        "target_language": target_language,
    }
