from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class TranslateRequest(BaseModel):
    text: str = Field(..., description="Text to translate")
    source_lang: Optional[str] = Field(None, description="Source language (auto-detect if None)")
    target_lang: str = Field(..., description="Target language code")

class BatchTranslateRequest(BaseModel):
    texts: List[str]
    source_lang: Optional[str] = None
    target_lang: str

class MarkupTranslateRequest(BaseModel):
    markup: str
    source_lang: Optional[str] = None
    target_lang: str

class DictionaryTranslateRequest(BaseModel):
    dictionary: Dict[str, str]
    source_lang: str
    target_lang: str

class QualitySummaryRequest(BaseModel):
    original: str
    translated: str
    source_lang: str
    target_lang: str

class UnsafeCheckRequest(BaseModel):
    text: str

class EmbeddingRequest(BaseModel):
    segments: List[str]

class AudioPreviewRequest(BaseModel):
    text: str
    lang: str
    output_path: str
