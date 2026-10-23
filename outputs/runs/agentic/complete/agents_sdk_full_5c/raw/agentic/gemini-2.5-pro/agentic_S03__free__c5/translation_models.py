from typing import List, Dict
from pydantic import BaseModel, Field

class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: str

class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: str

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    target_language: str
    source_language: str

class BatchTranslationResponse(BaseModel):
    translations: List[str]

class MarkupTranslationRequest(BaseModel):
    markup_content: str
    target_language: str
    source_language: str

class MarkupTranslationResponse(BaseModel):
    translated_markup_content: str

class DictionaryTranslationRequest(BaseModel):
    data: Dict[str, str]
    target_language: str
    source_language: str

class DictionaryTranslationResponse(BaseModel):
    translated_data: Dict[str, str]
