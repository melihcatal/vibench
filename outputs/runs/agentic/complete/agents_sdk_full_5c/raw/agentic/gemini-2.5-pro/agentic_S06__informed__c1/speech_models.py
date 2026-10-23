from typing import List, Optional
from pydantic import BaseModel, Field


class SpeechSynthesisRequest(BaseModel):
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str
    voice_name: Optional[str] = "en-US-Standard-C"


class VoiceDetail(BaseModel):
    name: str
    language_codes: List[str]
    ssml_gender: str


class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None


class SafetyAnalysisResult(BaseModel):
    is_safe: bool
    categories: dict = Field(default_factory=dict)


class EmbeddingResult(BaseModel):
    vectors: List[List[float]]


class TranscriptionResult(BaseModel):
    text: str
    confidence: float
