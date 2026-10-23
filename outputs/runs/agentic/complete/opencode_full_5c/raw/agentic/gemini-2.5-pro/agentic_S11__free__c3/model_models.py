from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ModelRequest:
    prompt: str
    model: str = "command-r"


@dataclass
class ModelResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class StreamedModelResponse:
    text_chunk: str
    provider_object: Any


@dataclass
class SafetyRating:
    is_safe: bool
    reasons: List[str]


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str


@dataclass
class EmbeddingResponse:
    embedding: List[float]


@dataclass
class AudioResponse:
    audio_content: bytes
