from pydantic import BaseModel
from typing import List, Dict, Optional

class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None

class MarkupTranslationRequest(BaseModel):
    markup: str
    target_language: str
    source_language: Optional[str] = None

class DictionaryTranslationRequest(BaseModel):
    dictionary: Dict[str, str]
    target_language: str
    source_language: Optional[str] = None

class TranslationResponse(BaseModel):
    translated_text: str

class BatchTranslationResponse(BaseModel):
    translations: List[str]

class MarkupTranslationResponse(BaseModel):
    translated_markup: str

class DictionaryTranslationResponse(BaseModel):
    translated_dictionary: Dict[str, str]