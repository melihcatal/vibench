from typing import Dict, Any
from google.cloud import translate_v2 as translate
import os


def localized_platform_output(text: str, target_language: str = "es") -> Dict[str, Any]:
    """
    Translates watsonx.ai model output to another locale using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS must be set.")

    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
        "provider": "Google Cloud Translation",
    }
