from typing import List, Dict, Optional
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = None


def normalize_language_code(language: str) -> str:
    language = language.lower()
    if language == "en":
        return "EN-US"
    elif language == "pt":
        return "PT-BR"
    elif language == "zh":
        return "ZH"
    return language.upper()
