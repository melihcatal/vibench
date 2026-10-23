import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any

def localized_platform_output(text_content: str, target_language: str = "es") -> Dict[str, Any]:
    """Translate platform model output for another locale using Google Cloud Translation API."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise for Google Cloud.
    translate_client = translate.Client()

    try:
        response = translate_client.translate(
            text_content, 
            target_language=target_language
        )
        
        return {
            "translated_text": response["translatedText"],
            "detected_source_language": response.get("detectedSourceLanguage"),
            "target_language": target_language
        }
    except Exception as e:
        raise RuntimeError(f"Google Cloud Translation API failed: {e}")
