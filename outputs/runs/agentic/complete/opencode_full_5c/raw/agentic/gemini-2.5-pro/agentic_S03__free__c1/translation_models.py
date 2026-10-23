from pydantic import BaseModel
from typing import List, Dict


class TranslationRequest(BaseModel):
    source_language: str
    target_language: str
    text: str


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: str


class BatchTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    texts: List[str]


class BatchTranslationResponse(BaseModel):
    translations: List[str]


class MarkupTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    markup: str


class MarkupTranslationResponse(BaseModel):
    translated_markup: str


class DictionaryTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    data: Dict[str, str]


class DictionaryTranslationResponse(BaseModel):
    translated_data: Dict[str, str]
