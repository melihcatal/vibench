import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate

def translate_appeal_text(text: str, target_language: str = "en", project_id: str = None) -> Dict[str, Any]:
    """Translates appeal text for review using Google Cloud Translation API."""
    
    if project_id is None:
        # Attempt to get project_id from environment variable if not provided
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if project_id is None:
            raise ValueError("Google Cloud Project ID not provided and not found in GOOGLE_CLOUD_PROJECT environment variable.")

    translate_client = translate.Client(project=project_id)

    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language
    }
