from typing import List, Dict, Optional
from pydantic import BaseModel

class TextTranslationRequest(BaseModel):
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

class TextTranslationResponse(BaseModel):
    translated_text: str
    source_language_code: str

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    target_language_code: str
    source_language_code: Optional[str] = None

class BatchTranslationResponse(BaseModel):
    translated_texts: List[str]
    source_language_code: str # Assuming a single source language for batch

class DictionaryTranslationRequest(BaseModel):
    input_dict: Dict[str, str]
    target_language_code: str
    source_language_code: Optional[str] = None

class DictionaryTranslationResponse(BaseModel):
    translated_dict: Dict[str, str]
    source_language_code: str
