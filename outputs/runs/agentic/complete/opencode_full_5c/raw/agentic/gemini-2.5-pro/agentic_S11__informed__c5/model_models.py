from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ModelRequest(BaseModel):
    prompt: str


class ModelResponse(BaseModel):
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SafetyAnalysis(BaseModel):
    hate: int
    self_harm: int
    sexual: int
    violence: int


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = None


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class AudioResponse(BaseModel):
    audio_content: bytes
