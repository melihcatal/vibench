from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 256
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Any = None


@dataclass
class StreamChunk:
    text: str
    raw: Any = None


@dataclass
class SafetyResult:
    flagged: bool
    categories: List[str] = field(default_factory=list)
    raw: Any = None


@dataclass
class TranslationResult:
    text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Any = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    raw: Any = None


@dataclass
class AudioResult:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "content", "output", "message"):
            if key in value:
                return normalize_text(value[key])
    if isinstance(value, Iterable):
        parts = [normalize_text(item) for item in value]
        return "".join(part for part in parts if part)
    return str(value).strip()
