import os
from typing import Optional
from translation_client import get_translation_client, get_location_path
from translation_models import TranslationRequest, TranslationResponse

def translate_single_text(
    text: str,
    target_language_code: str,
    source_language_code: Optional[str] = None
) -> TranslationResponse:
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    parent = get_location_path(project_id, location)
    
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
            "mime_type": "text/plain",
        }
    )
    
    translations = [t.translated_text for t in response.translations]
    detected_source = response.translations[0].detected_language_code if response.translations else None
    
    return TranslationResponse(translations=translations, detected_source_language_code=detected_source)