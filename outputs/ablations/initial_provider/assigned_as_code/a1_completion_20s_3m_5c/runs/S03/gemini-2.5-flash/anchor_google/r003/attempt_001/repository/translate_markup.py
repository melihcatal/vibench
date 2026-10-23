from translation_client import get_translation_client, get_parent_path
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(payload: TranslationRequest, config: dict = None) -> TranslationResponse:
    config = config or {}
    client = get_translation_client()
    parent = get_parent_path(config['project_id'], config.get('location', 'global'))

    if not isinstance(payload.text, str):
        raise ValueError("payload.text must be a string for markup translation.")

    # Ensure mime_type is set to text/html for markup translation
    payload.mime_type = "text/html"

    response = client.translate_text(request={
        "parent": parent,
        "contents": [payload.text],
        "mime_type": payload.mime_type,
        "source_language_code": payload.source_language,
        "target_language_code": payload.target_language,
    })
    return TranslationResponse(
        translated_text=response.translations[0].translated_text,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
