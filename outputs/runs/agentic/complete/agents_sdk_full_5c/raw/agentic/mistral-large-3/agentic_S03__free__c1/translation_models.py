from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    model: str = "google-translate-ai-v3"
    glossary_id: Optional[str] = None
    format_: Optional[str] = None

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    source_lang: str
    target_lang: str
    model: str = "google-translate-ai-v3"
    glossary_id: Optional[str] = None

class TranslationResponse(BaseModel):
    translated_text: str

class BatchTranslationResponse(BaseModel):
    translated_texts: List[str]