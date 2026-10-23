from typing import Dict, List, Optional, TypedDict, Union
from dataclasses import dataclass


class TranslationRequest(TypedDict):
    text: Union[str, List[str]]
    target_language: str
    source_language: Optional[str]


class TranslationResponse(TypedDict):
    translated_text: Union[str, List[str]]


@dataclass
class TranslationError:
    error: str
    details: Optional[Dict] = None


def normalize_language_code(language_code: str) -> str:
    """Normalize language codes to ISO 639-1 format for Google Cloud Translation."""
    if len(language_code) == 2:
        return language_code.lower()
    elif len(language_code) == 5 and language_code[2] == "-":
        return language_code[:2].lower()
    return language_code.lower()
