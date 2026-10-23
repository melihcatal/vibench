from google.cloud import translate
from typing import List, Dict, Any
import os

def translate_runbook_notes(notes: List[str], target_language: str = "en") -> List[Dict[str, Any]]:
    # Google Cloud project ID must be set as an environment variable or configured.
    # For this example, we assume GOOGLE_CLOUD_PROJECT is set.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global"  # Or a specific region, e.g., "us-central1"

    parent = f"projects/{project_id}/locations/{location}"

    translated_results = []
    for note in notes:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [note],
                "target_language_code": target_language,
            }
        )
        
        for translation in response.translations:
            translated_results.append({"original_text": note, "translated_text": translation.translated_text, "target_language": target_language})
            
    return translated_results
