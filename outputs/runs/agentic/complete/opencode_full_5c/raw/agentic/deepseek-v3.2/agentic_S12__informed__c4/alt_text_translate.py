import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_image_description(
    description: str, target_language: str = "es"
) -> Dict[str, Any]:
    """
    Translate generated image descriptions using Google Cloud Translation.

    Args:
        description: Image description text to translate
        target_language: Target language code (default: Spanish)

    Returns:
        Dictionary containing original and translated text
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    client = translate.Client()

    result = client.translate(description, target_language=target_language)

    return {
        "original": description,
        "translated": result["translatedText"],
        "target_language": target_language,
        "detected_language": result.get("detectedSourceLanguage", "en"),
    }
