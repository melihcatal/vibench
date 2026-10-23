from typing import List, Dict
from pydantic import BaseModel

class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = "auto"

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    target_language: str
    source_language: str = "auto"

class MarkupTranslationRequest(TranslationRequest):
    format: str = "html"

class DictionaryTranslationRequest(BaseModel):
    data: Dict[str, str]
    target_language: str
    source_language: str = "auto"

class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: str
    original_text: str

class BatchTranslationResponse(BaseModel):
    translations: List[TranslationResponse]

class DictionaryTranslationResponse(BaseModel):
    translated_data: Dict[str, str]
    detected_source_language: str # Assuming one for the batch for simplicity
