from typing import Optional

from translation_client import translate_single_text
from translation_models import (
    TranslationRequest,
    TranslationResult,
    parse_google_translate_response,
)


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "nmt",
    api_key: Optional[str] = None,
) -> TranslationResult:
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        format="text",
        model=model,
    )

    response_data = translate_single_text(
        text=request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        format_type=request.format,
        model=request.model,
        api_key=api_key,
    )

    return parse_google_translate_response(response_data, request.text)


def translate_text_with_config(
    config: TranslationRequest,
    api_key: Optional[str] = None,
) -> TranslationResult:
    return translate_text(
        text=config.text,
        target_language=config.target_language,
        source_language=config.source_language,
        model=config.model,
        api_key=api_key,
    )
