import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def record_translate(document_data: Dict[str, Any], target_language: str, project_id: str = None) -> Dict[str, Any]:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and not found in GOOGLE_CLOUD_PROJECT environment variable.")

    translate_client = translate.Client(project=project_id)

    translated_document = document_data.copy()

    # Assuming user-facing fields are nested under a 'user_facing_text' key or similar
    # For simplicity, let's assume a field named 'description' and 'title' need translation
    fields_to_translate = ["description", "title"]

    for field in fields_to_translate:
        if field in translated_document and isinstance(translated_document[field], str):
            text = translated_document[field]
            result = translate_client.translate(text, target_language=target_language)
            translated_document[f"{field}_translated_{target_language}"] = result["translatedText"]

    return translated_document
