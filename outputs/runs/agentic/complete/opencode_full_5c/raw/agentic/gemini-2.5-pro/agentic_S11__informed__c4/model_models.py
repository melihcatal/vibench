from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class ModelRequest:
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1024


@dataclass
class ModelResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class StreamChunk:
    text: str
    raw_chunk: Optional[Dict[str, Any]] = None


@dataclass
class SafetyResult:
    is_safe: bool
    details: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str


@dataclass
class EmbeddingResult:
    embedding: List[float]


@dataclass
class AudioResult:
    audio_content: bytes
