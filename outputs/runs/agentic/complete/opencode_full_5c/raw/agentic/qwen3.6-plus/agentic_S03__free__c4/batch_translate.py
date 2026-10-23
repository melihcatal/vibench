from typing import Optional

from translation_client import translate_batch_texts
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    TranslationResult,
    parse_google_translate_response,
)


def batch_translate(
    texts: list[str],
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "nmt",
    api_key: Optional[str] = None,
) -> BatchTranslationResult:
    request = BatchTranslationRequest(
        texts=texts,
        source_language=source_language,
        target_language=target_language,
        format="text",
        model=model,
    )

    response_data_list = translate_batch_texts(
        texts=request.texts,
        target_language=request.target_language,
        source_language=request.source_language,
        format_type=request.format,
        model=request.model,
        api_key=api_key,
    )

    results: list[TranslationResult] = []
    for i, response_data in enumerate(response_data_list):
        result = parse_google_translate_response(response_data, request.texts[i])
        results.append(result)

    return BatchTranslationResult(results=results)


def batch_translate_with_config(
    config: BatchTranslationRequest,
    api_key: Optional[str] = None,
) -> BatchTranslationResult:
    return batch_translate(
        texts=config.texts,
        target_language=config.target_language,
        source_language=config.source_language,
        model=config.model,
        api_key=api_key,
    )
