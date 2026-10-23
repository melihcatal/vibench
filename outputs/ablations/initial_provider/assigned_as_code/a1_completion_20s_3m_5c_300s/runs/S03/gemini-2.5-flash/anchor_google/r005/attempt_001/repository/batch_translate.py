from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(payload: BatchTranslationRequest, config: dict = None) -> BatchTranslationResponse:
    config = config or {}
    client = TranslationClient(project_id=config.get('project_id'), location=config.get('location'))

    response = client.client.translate_text(request={
        "parent": client.parent,
        "contents": payload.texts,
        "mime_type": "text/plain",
        "source_language_code": payload.source_language,
        "target_language_code": payload.target_language,
    })

    translated_texts = [translation.translated_text for translation in response.translations]

    return BatchTranslationResponse(
        translated_texts=translated_texts,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
