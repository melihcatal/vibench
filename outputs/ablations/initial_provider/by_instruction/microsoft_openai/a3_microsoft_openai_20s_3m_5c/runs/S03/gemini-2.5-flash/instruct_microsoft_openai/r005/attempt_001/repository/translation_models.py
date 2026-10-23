from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TranslationRequest:
    text: str | List[str]
    source_language: str
    target_language: str
    text_type: str = "plain"

@dataclass
class TranslationResponse:
    translated_text: str | List[str]
    detected_source_language: str | None = None

@dataclass
class MarkupTranslationRequest(TranslationRequest):
    text_type: str = "html"

@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, Any]
    source_language: str
    target_language: str

@dataclass
class DictionaryTranslationResponse:
    translated_data: Dict[str, Any]

# Helper for normalizing language codes if needed across different APIs
def normalize_language_code(lang_code: str, api_type: str = "openai") -> str:
    """
    Normalizes language codes for different APIs if necessary.
    This is a placeholder and can be expanded based on specific API requirements.
    """
    if api_type == "deepl":
        return lang_code.upper() # DeepL often uses uppercase codes
    elif api_type == "aws" or api_type == "google":
        return lang_code.lower() # AWS/Google often use lowercase codes
    return lang_code
