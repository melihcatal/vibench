from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ModelRequest:
    prompt: str
    context: Optional[str] = None
    model: Optional[str] = None


@dataclass
class ModelResponse:
    text: str
    raw_response: Any


@dataclass
class StreamChunk:
    text: str
    raw_response: Any


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    scores: Dict[str, float]
    raw_response: Any


@dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    raw_response: Any


@dataclass
class EmbeddingRequest:
    text: str
    model: Optional[str] = None


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    raw_response: Any


@dataclass
class TTSRequest:
    text: str
    voice_id: Optional[str] = None


@dataclass
class TTSResponse:
    audio_content: bytes
    raw_response: Any
