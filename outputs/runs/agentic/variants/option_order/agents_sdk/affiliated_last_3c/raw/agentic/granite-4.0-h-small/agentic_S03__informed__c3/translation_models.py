import os
from typing import List, Dict

def validate_language_code(lang: str) -> str:
    """Ensures language code is a non-empty string.
    Raises ValueError for invalid input."""
    if not lang or not isinstance(lang, str):
        raise ValueError('Language code must be a non-empty string.')
    return lang


def validate_text(text: str) -> str:
    """Simple validation: ensure input is a string and not empty after stripping.
    Raises ValueError if validation fails."""
    if not isinstance(text, str):
        raise TypeError('Input must be a string')
    trimmed = text.strip()
    if not trimmed:
        raise ValueError('Input text cannot be empty or whitespace only')
    return trimmed


def batch_split(texts: List[str], max_batch_size: int = 1000) -> List[List[str]]:
    """Splits a list of texts into chunks of at most max_batch_size items."""
    return [texts[i:i + max_batch_size] for i in range(0, len(texts), max_batch_size)]
