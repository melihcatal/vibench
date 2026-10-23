from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = TranslationClient()
    translate_client = client.get_client()
    parent = client.get_parent()

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": request.texts,
            "target_language_code": request.target_language,
            "source_language_code": request.source_language,
            "mime_type": request.mime_type,
        }
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    detected_source_languages = [
        translation.detected_language_code for translation in response.translations
    ]

    return BatchTranslationResponse(translated_texts, detected_source_languages)
