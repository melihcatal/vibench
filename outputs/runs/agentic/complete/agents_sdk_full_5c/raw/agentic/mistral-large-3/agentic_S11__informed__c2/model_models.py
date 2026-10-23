from typing import Dict, Any, Optional, Iterator
from pydantic import BaseModel


class ModelRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1024


class ModelResponse(BaseModel):
    output: str
    metadata: Dict[str, Any] = {}


class ModelResponseWithMetadata(BaseModel):
    output: str
    metadata: Dict[str, Any]


class StreamChunk(BaseModel):
    text: str
    metadata: Dict[str, Any] = {}


class SafetyCheckRequest(BaseModel):
    text: str


class SafetyCheckResponse(BaseModel):
    is_safe: bool
    violations: Dict[str, Any] = {}


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_text: str


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: list[float]
    model_id: str


class AudioRequest(BaseModel):
    text: str
    voice: str = "en-US-Wavenet-D"


class AudioResponse(BaseModel):
    audio_content: bytes