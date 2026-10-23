import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_consent_copy(text: str, target_language: str) -> Dict[str, Any]:
    # Google Cloud Translation API client initialization
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    try:
        client = translate.Client()
    except Exception as e:
        return {"status": "error", "message": f"Failed to initialize Google Cloud Translation client. Ensure GOOGLE_APPLICATION_CREDENTIALS is set: {e}"}

    try:
        result = client.translate(text, target_language=target_language)

        translated_text = result["translatedText"]
        source_language = result["detectedSourceLanguage"]

        return {
            "status": "success",
            "original_text": text,
            "translated_text": translated_text,
            "source_language": source_language,
            "target_language": target_language,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
