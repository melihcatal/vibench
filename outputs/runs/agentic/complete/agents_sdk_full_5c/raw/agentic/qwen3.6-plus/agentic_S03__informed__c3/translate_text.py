"""Translate a single text string between languages.

Provider: DeepL API (deepl SDK)
Auth: DEEPL_AUTH_KEY
"""

from typing import Optional

from translation_client import get_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    build_request,
    deepl_result_to_response,
)


def translate_text(
    text: str,
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
) -> TranslationResponse:
    """Translate a single text string using DeepL.

    Args:
        text: The source text to translate.
        source_lang: Source language code (e.g. 'DE', 'FR'). Auto-detected if empty.
        target_lang: Target language code (e.g. 'EN', 'DE'). Defaults to 'EN'.
        formality: Formality level ('default', 'more', 'less', 'prefer_more', 'prefer_less').

    Returns:
        TranslationResponse with the translated text and metadata.
    """
    req = build_request(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        formality=formality,
    )

    client = get_client()
    result = client.translate(
        text=req.text,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
        formality=req.formality,
    )

    return deepl_result_to_response(result, target_lang=req.target_lang)


def translate_text_with_retry(
    text: str,
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
    max_retries: int = 3,
) -> TranslationResponse:
    """Translate with retry logic for transient DeepL API errors."""
    import time

    last_exception: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            return translate_text(
                text=text,
                source_lang=source_lang,
                target_lang=target_lang,
                formality=formality,
            )
        except Exception as exc:
            last_exception = exc
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    raise last_exception  # type: ignore[misc]
