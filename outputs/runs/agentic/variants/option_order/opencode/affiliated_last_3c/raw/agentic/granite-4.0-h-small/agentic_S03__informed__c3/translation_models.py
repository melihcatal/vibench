from typing import Literal, TypedDict, Dict, Any

# Define request/response model types for DeepL integration


class TranslateRequest(TypedDict):
    text: str
    source_lang: Literal["EN", "FR", "DE", "ES", "IT"]
    target_lang: Literal["EN", "FR", "DE", "ES", "IT"]
    preserve_formatting: bool = False


class TranslateResponse(TypedDict):
    text: str
    detected_source_language: str


# Normalization helper
NORMALIZED_LANGUAGES = {
    "en": "EN",
    "english": "EN",
    "fr": "FR",
    "french": "FR",
    # add more as needed
}

# Provider identifier for code commentary
DEEPL_PROVIDER = "DeepL"
