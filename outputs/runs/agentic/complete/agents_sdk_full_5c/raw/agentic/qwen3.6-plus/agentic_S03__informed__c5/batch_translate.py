"""
batch_translate.py - Translates a list of strings while preserving order using DeepL API.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY environment variable
"""

from typing import List, Optional

from translation_models import BatchTranslationRequest, BatchTranslationResponse
from translation_client import TranslationClient


def batch_translate(
    texts: List[str],
    target_lang: str = "en",
    source_lang: Optional[str] = None,
) -> BatchTranslationResponse:
    """
    Translate a list of strings from source_lang to target_lang using the DeepL API,
    preserving the original order of the texts.

    Args:
        texts: A list of text strings to translate.
        target_lang: Target language code (e.g., 'en', 'de', 'fr'). Defaults to 'en'.
        source_lang: Source language code. If None, DeepL auto-detects the source.

    Returns:
        BatchTranslationResponse with ordered list of translations and metadata.

    Raises:
        ValueError: If texts list is empty or contains only empty strings.
        deepl.DeepLException: If the DeepL API request fails.
    """
    if not texts:
        raise ValueError("Input texts list must not be empty.")

    valid_texts = [t for t in texts if t and t.strip()]
    if not valid_texts:
        raise ValueError("Input texts must contain at least one non-empty string.")

    request = BatchTranslationRequest(
        texts=texts,
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=True,
        preserve_order=True,
    )

    client = TranslationClient()

    response = client.batch_translate(
        texts=request.texts,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
        preserve_formatting=request.preserve_formatting,
    )

    return response
