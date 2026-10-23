from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class LLMRequest:
    model_family: str
    messages: List[ChatMessage]
    temperature: float = 0.2
    max_tokens: int = 512
    top_p: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    text: str
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class StreamingChunk:
    text: str
    done: bool = False
    raw: Any = None


@dataclass
class NormalizedEmbedding:
    vector: List[float]
    model: str
    raw: Any = None


@dataclass
class SafetyResult:
    flagged: bool
    category: Optional[str] = None
    score: Optional[float] = None
    raw: Any = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Any = None


@dataclass
class AudioResult:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    raw: Any = None
