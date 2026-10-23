from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    max_tokens: int = 512
    temperature: float = 0.2
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResponse:
    text: str
    usage: Dict[str, Any] = field(default_factory=dict)
    resource_id: Optional[str] = None
    model_id: Optional[str] = None
    raw: Any = None


@dataclass
class StreamChunk:
    text: str
    raw: Any = None


@dataclass
class SafetyResult:
    unsafe: bool
    score: float
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Any = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    model_id: Optional[str] = None
    raw: Any = None


@dataclass
class AudioResult:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    raw: Any = None


def normalize_text(parts: Iterable[Any]) -> str:
    text_parts: List[str] = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, str):
            text_parts.append(part)
        elif isinstance(part, dict) and "text" in part:
            text_parts.append(str(part["text"]))
        else:
            text_parts.append(str(part))
    return "".join(text_parts).strip()
