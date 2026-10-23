from translation_client import translate_batch
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(
    texts: list[str],
    source_language: str,
    target_language: str,
    formality: str | None = None,
) -> BatchTranslationResponse:
    request = BatchTranslationRequest(
        texts=texts,
        source_language=source_language,
        target_language=target_language,
        formality=formality,
    )
    result = translate_batch(
        texts=request.texts,
        source_language=request.source_language,
        target_language=request.target_language,
        formality=request.formality,
        preserve_formatting=request.preserve_formatting,
    )
    return result
