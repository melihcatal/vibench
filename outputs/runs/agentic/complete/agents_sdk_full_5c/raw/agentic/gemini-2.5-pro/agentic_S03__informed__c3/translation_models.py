from pydantic import BaseModel, Field
from typing import List, Dict

class TranslationRequest(BaseModel):
    source_language: str
    target_language: str
    content: List[str]

class TranslationResponse(BaseModel):
    translated_texts: List[str]

class DictionaryTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    content: Dict[str, str]

class DictionaryTranslationResponse(BaseModel):
    translated_content: Dict[str, str]

class MarkupTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    html_content: str

class MarkupTranslationResponse(BaseModel):
    translated_html: str
