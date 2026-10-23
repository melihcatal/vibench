from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class ChatRequest:
    model_family: str
    system: str = ""
    user: str = ""
    context: str = ""
    temperature: float = 0.2
    max_tokens: int = 512
    response_format: Optional[Dict[str, Any]] = None
    stream: bool = False


@dataclass
class ChatResponse:
    text: str
    raw: Any = None
    model: str = ""
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JsonExtraction:
    data: Dict[str, Any]
    raw_text: str = ""


@dataclass
class ModerationResult:
    provider: str
    flagged: bool
    scores: Dict[str, float] = field(default_factory=dict)
    raw: Any = None


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str = ""
    target_language: str = "en"
    raw: Any = None


@dataclass
class EmbeddingResult:
    input_text: str
    vector: List[float]
    model: str = ""
    raw: Any = None


@dataclass
class SpeechResult:
    text: str
    audio_bytes: bytes
    voice: str = ""
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Mapping) and "text" in value:
        return normalize_text(value["text"])
    if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray)):
        return "\n".join(normalize_text(item) for item in value if normalize_text(item))
    return str(value).strip()
