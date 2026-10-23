import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_invoice_note(note_text: str, target_language: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    # Google Cloud Translation API client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials from the environment.
    # No specific project_id or location is required for v2 API client initialization
    # but it's good practice to have them configured for the environment.

    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            note_text, target_language=target_language)
        translated_text = result['translatedText']
        detected_source_language = result['detectedSourceLanguage']
        return {
            "translated_text": translated_text,
            "source_language": detected_source_language,
            "target_language": target_language
        }
    except Exception as e:
        return {"error": f"Failed to translate invoice note: {str(e)}"}
