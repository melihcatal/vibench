from typing import List, Dict, Any
from google.cloud import translate_v3
from translation_client import get_translation_service_client, get_project_id, get_location
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate_text(payload: BatchTranslationRequest, config: Dict[str, Any] = None) -> BatchTranslationResponse:
    config = config or {}
    client = get_translation_service_client()
    project_id = config.get("project_id", get_project_id())
    location = config.get("location", get_location())
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(request={
        "parent": parent,
        "contents": payload.texts,
        "mime_type": "text/plain",
        "source_language_code": payload.source_language,
        "target_language_code": payload.target_language,
    })

    translated_texts = [translation.translated_text for translation in response.translations]

    return BatchTranslationResponse(
        translations=translated_texts,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
