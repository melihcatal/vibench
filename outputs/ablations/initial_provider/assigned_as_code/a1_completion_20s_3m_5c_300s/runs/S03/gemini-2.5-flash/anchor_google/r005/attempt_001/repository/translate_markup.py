from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse


def translate_markup(payload: TranslationRequest, config: dict = None) -> TranslationResponse:
    config = config or {}
    client = TranslationClient(project_id=config.get('project_id'), location=config.get('location'))

    response = client.client.translate_text(request={
        "parent": client.parent,
        "contents": [payload.text],
        "mime_type": "text/html",
        "source_language_code": payload.source_language,
        "target_language_code": payload.target_language,
    })

    return TranslationResponse(
        text=response.translations[0].translated_text,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
