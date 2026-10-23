from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class TranslationRequest:
    """
    A request model for translation tasks.
    """

    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    """
    A request model for batch translation tasks.
    """

    texts: List[str]
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    """
    A response model for translation tasks.
    """

    translated_text: str


@dataclass
class BatchTranslationResponse:
    """
    A response model for batch translation tasks.
    """

    translated_texts: List[str]


def normalize_language_code(language_code: str) -> str:
    """
    Normalizes language codes to the format expected by Google Cloud Translation.

    Args:
        language_code: The language code to normalize (e.g., 'en-US', 'en').

    Returns:
        The normalized language code.
    """
    return language_code.split("-")[0].lower()
