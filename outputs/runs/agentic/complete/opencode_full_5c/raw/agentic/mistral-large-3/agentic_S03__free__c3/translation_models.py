from typing import Dict, List, Optional, TypedDict, Union
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: Union[str, List[str]]
    target_language: str
    source_language: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: Union[str, List[str]]
    detected_source_language: Optional[str] = None


class MarkupTranslationRequest(BaseModel):
    markup: str
    target_language: str
    source_language: Optional[str] = None
    protected_tags: Optional[List[str]] = None


class DictionaryTranslationRequest(BaseModel):
    dictionary: Dict[str, str]
    target_language: str
    source_language: Optional[str] = None


def normalize_language_code(language_code: str) -> str:
    return language_code.split("-")[0].lower()
