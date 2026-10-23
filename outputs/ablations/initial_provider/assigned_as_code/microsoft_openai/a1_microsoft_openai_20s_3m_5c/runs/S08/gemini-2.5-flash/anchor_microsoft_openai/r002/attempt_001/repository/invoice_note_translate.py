import os
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate

def translate_invoice_notes(notes: List[str], target_language: str = 'en', config: Dict[str, Any] = None) -> List[Dict[str, str]]:
    config = config or {}
    # The Google Cloud Translation API client automatically picks up project ID and credentials
    # from environment variables (e.g., GOOGLE_APPLICATION_CREDENTIALS) or the GKE environment.
    # No explicit project_id or location is usually required for client initialization.

    client = translate.Client()

    translated_results = []
    for note in notes:
        if not note or not isinstance(note, str):
            translated_results.append({"original_text": note, "translated_text": note, "detected_source_language": None})
            continue

        result = client.translate(note, target_language=target_language)
        translated_results.append({
            "original_text": note,
            "translated_text": result['translatedText'],
            "detected_source_language": result['detectedSourceLanguage']
        })

    return translated_results
