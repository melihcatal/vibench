# translation_models.py
from typing import TypedDict, List


class TranslateRequest(TypedDict):
    """Standardized request payload for translation operations."""

    text: str
    source_lang: str
    target_lang: str


class TranslateResponse(TypedDict):
    """Standardized response payload containing translated text."""

    translated_text: str


class BatchTranslateResponse(List[TranslateResponse]):
    """Wrapper for list of TranslateResponse objects."""


# Normalization helper to ensure consistent payload shape
MODELS = {
    "text": TranslateRequest,
    "batch": BatchTranslateResponse,
    "markup": TranslateRequest,
    "dict": TranslateRequest,
}
