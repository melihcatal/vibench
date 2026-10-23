from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class TranslationRequest(BaseModel):
    """A single text translation request."""
    text: str = Field(..., description="The text to translate.")
    target_language: str = Field(..., description="The target language code (e.g., 'es').")
    source_language: Optional[str] = Field(None, description="The source language code (e.g., 'en').")

class TranslationResponse(BaseModel):
    """A single text translation result."""
    translated_text: str
    detected_source_language: Optional[str] = None

class BatchTranslationRequest(BaseModel):
    """A batch translation request for multiple texts."""
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None

class BatchTranslationResponse(BaseModel):
    """A batch translation result."""
    translations: List[TranslationResponse]

class DictionaryTranslationRequest(BaseModel):
    """A request to translate the values of a dictionary."""
    data: Dict[str, str]
    target_language: str
    source_language: Optional[str] = None

class DictionaryTranslationResponse(BaseModel):
    """The result of translating dictionary values."""
    translated_data: Dict[str, str]
