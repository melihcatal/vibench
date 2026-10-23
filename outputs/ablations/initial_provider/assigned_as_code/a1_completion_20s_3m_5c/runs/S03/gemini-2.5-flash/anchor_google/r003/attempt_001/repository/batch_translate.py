from translation_client import get_translation_client, get_parent_path
from translation_models import TranslationRequest, TranslationResponse
from typing import List

def batch_translate(payload: TranslationRequest, config: dict = None) -> TranslationResponse:
    config = config or {}
    client = get_translation_client()
    parent = get_parent_path(config['project_id'], config.get('location', 'global'))

    if not isinstance(payload.text, list):
        raise ValueError("payload.text must be a list for batch translation.")

    response = client.translate_text(request={
        "parent": parent,
        "contents": payload.text,
        "mime_type": payload.mime_type,
        "source_language_code": payload.source_language,
        "target_language_code": payload.target_language,
    })

    translated_texts = [translation.translated_text for translation in response.translations]

    return TranslationResponse(
        translated_text=translated_texts,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
