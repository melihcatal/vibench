from translation_client import GoogleTranslateClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client_wrapper = GoogleTranslateClient()
    client = client_wrapper.get_client()
    parent = client_wrapper.get_parent()

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": request.texts,
            "target_language_code": request.target_language,
            "source_language_code": request.source_language
            if request.source_language
            else None,
            "mime_type": "text/plain",
        }
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    detected_languages = [
        translation.detected_language_code for translation in response.translations
    ]

    return BatchTranslationResponse(
        translated_texts=translated_texts, detected_source_languages=detected_languages
    )
