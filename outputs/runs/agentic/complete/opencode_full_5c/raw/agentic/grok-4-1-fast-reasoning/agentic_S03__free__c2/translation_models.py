from typing import TypedDict, List, Optional


class SingleTranslateRequest(TypedDict):
    text: str
    source_lang: Optional[str]
    target_lang: str


class BatchTranslateRequest(TypedDict):
    texts: List[str]
    source_lang: Optional[str]
    target_lang: str


def normalize_language_code(lang: str) -> str:
    """
    Normalize language code to DeepL format.
    DeepL uses uppercase two-letter ISO 639-1 codes (e.g., 'EN', 'FR').
    """
    return lang.upper()[:2]
