from typing import List
from translation_client import get_translate_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse
from google.cloud import translate_v3beta1 as translate


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = get_translate_client()
    parent = f"projects/{client.project}"

    response = client.translate_text(
        request=translate.TranslateTextRequest(
            parent=parent,
            contents=request.texts,
            target_language_code=request.target_language,
            source_language_code=request.source_language
            if request.source_language
            else None,
            mime_type="text/plain",
        )
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    detected_source_languages = [
        translation.detected_language_code for translation in response.translations
    ]

    return BatchTranslationResponse(
        translated_texts=translated_texts,
        detected_source_languages=detected_source_languages,
    )
