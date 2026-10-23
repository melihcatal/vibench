from translation_client import translate_text_values
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    normalize_text,
    normalize_text_list,
)


def batch_translate(
    texts, source_language: str, target_language: str
) -> BatchTranslationResponse:
    request = BatchTranslationRequest(
        texts=normalize_text_list(texts),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target_language),
    )
    translated_texts = translate_text_values(
        request.texts, request.source_language, request.target_language
    )
    return BatchTranslationResponse(
        translated_texts=translated_texts,
        source_language=request.source_language,
        target_language=request.target_language,
    )
