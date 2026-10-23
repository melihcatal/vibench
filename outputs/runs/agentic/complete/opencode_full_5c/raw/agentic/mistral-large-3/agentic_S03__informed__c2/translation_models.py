from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: Union[str, List[str]]
    target_language: str
    source_language: Optional[str] = None
    format_: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: Union[str, List[str]]
    detected_source_language: Optional[str] = None
    model_used: Optional[str] = None


def normalize_language_code(language: str) -> str:
    language = language.lower()
    if language == "en":
        return "en"
    elif language == "es":
        return "es"
    elif language == "fr":
        return "fr"
    elif language == "de":
        return "de"
    elif language == "zh" or language == "zh-cn":
        return "zh-CN"
    elif language == "ja":
        return "ja"
    elif language == "ko":
        return "ko"
    elif language == "ar":
        return "ar"
    elif language == "ru":
        return "ru"
    elif language == "pt":
        return "pt"
    elif language == "it":
        return "it"
    else:
        return language
