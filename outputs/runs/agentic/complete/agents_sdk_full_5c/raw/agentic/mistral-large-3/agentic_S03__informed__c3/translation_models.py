from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class TranslationRequest(BaseModel):
    text: str
    source_lang: Optional[str] = None
    target_lang: str

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    source_lang: Optional[str] = None
    target_lang: str

class MarkupTranslationRequest(BaseModel):
    markup: str
    source_lang: Optional[str] = None
    target_lang: str
    tag_handling: str = "xml"
    ignore_tags: List[str] = []

class DictionaryTranslationRequest(BaseModel):
    dictionary: Dict[str, str]
    source_lang: Optional[str] = None
    target_lang: str

class TranslationResponse(BaseModel):
    translated_text: str

class BatchTranslationResponse(BaseModel):
    translations: List[str]

class MarkupTranslationResponse(BaseModel):
    translated_markup: str

class DictionaryTranslationResponse(BaseModel):
    translated_dictionary: Dict[str, str]