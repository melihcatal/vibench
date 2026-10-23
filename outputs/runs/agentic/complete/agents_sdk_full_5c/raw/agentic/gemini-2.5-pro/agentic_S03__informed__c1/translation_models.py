"""
Local request, response, and normalization helpers for General Text Translation.
"""
from typing import List, Dict
from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    source_language: str
    target_language: str
    texts: List[str]


class TranslationResponse(BaseModel):
    translations: List[str]


class DictionaryTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    data: Dict[str, str]


class DictionaryTranslationResponse(BaseModel):
    translated_data: Dict[str, str]


class MarkupTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    markup_content: str
    
class MarkupTranslationResponse(BaseModel):
    translated_markup: str
