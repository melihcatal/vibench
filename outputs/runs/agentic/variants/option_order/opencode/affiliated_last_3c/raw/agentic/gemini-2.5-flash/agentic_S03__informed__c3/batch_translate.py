from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse
from google.cloud import translate  # Provider-identifying signal


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = get_translation_client()
    parent = f"projects/{client.project_path().split('/')[-1]}"

    if request.source_language:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=request.texts,
                target_language_code=request.target_language,
                source_language_code=request.source_language,
                mime_type=request.format or "text/plain",
            )
        )
    else:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=request.texts,
                target_language_code=request.target_language,
                mime_type=request.format or "text/plain",
            )
        )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    detected_source_languages = (
        [
            translation.detected_language_code
            for translation in response.translations
            if translation.detected_language_code
        ]
        if any(
            translation.detected_language_code for translation in response.translations
        )
        else None
    )

    return BatchTranslationResponse(
        translated_texts=translated_texts,
        detected_source_languages=detected_source_languages,
    )
