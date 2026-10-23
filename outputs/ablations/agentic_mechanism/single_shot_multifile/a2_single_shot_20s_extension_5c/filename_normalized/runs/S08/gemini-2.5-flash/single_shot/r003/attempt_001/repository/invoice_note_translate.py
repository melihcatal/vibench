import os
from google.cloud import translate_v3 as translate
from document_client import get_google_translate_client
from document_models import TranslationRequest

def translate_invoice_notes(request: TranslationRequest) -> str:
    if not request.text:
        return ""

    client = get_google_translate_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set for translation")

    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [request.text],
                "target_language_code": request.target_language_code,
                "source_language_code": request.source_language_code,
                "model": "projects/PROJECT_ID/locations/LOCATION_ID/models/MODEL_ID",
            }
        )
        if response.translations:
            return response.translations[0].translated_text
        return ""
    except Exception as e:
        return f"Error translating: {e}"