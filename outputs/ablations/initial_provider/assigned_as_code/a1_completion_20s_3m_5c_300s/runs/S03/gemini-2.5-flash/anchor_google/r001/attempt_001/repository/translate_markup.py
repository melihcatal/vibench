from typing import Dict, Any
from google.cloud import translate_v3
from translation_client import get_translation_service_client, get_project_id, get_location
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse

def translate_markup(payload: MarkupTranslationRequest, config: Dict[str, Any] = None) -> MarkupTranslationResponse:
    config = config or {}
    client = get_translation_service_client()
    project_id = config.get("project_id", get_project_id())
    location = config.get("location", get_location())
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(request={
        "parent": parent,
        "contents": [payload.markup_text],
        "mime_type": payload.mime_type,
        "source_language_code": payload.source_language,
        "target_language_code": payload.target_language,
    })

    translated_markup_text = response.translations[0].translated_text

    return MarkupTranslationResponse(
        translated_markup_text=translated_markup_text,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
