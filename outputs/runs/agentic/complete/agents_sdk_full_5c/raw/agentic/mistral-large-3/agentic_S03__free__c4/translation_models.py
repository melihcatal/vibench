from typing import Optional, List
from pydantic import BaseModel

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    formality: Optional[str] = None

class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str
    detected_language_code: Optional[str] = None

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    source_lang: str
    target_lang: str

class BatchTranslationResponse(BaseModel):
    translations: List[TranslationResponse]

class MarkupTranslationRequest(BaseModel):
    markup: str
    source_lang: str
    target_lang: str
    formality: Optional[str] = None

class DictionaryTranslationRequest(BaseModel):
    dictionary: dict
    source_lang: str
    target_lang: str
    formality: Optional[str] = None