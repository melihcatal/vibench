from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class LLMRequest:
    model: str
    messages: List[Dict[str, str]]
    temperature: float = 0.2
    max_tokens: int = 512
    top_p: float = 1.0


@dataclass
class LLMResponse:
    text: str
    model: str
    raw: Any = None


@dataclass
class NormalizedTextResult:
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedJSONResult:
    content: Dict[str, Any]
    raw_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyResult:
    unsafe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Any = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    raw: Any = None


@dataclass
class TranslationResult:
    text: str
    target_language: str
    raw: Any = None


@dataclass
class SpokenBriefResult:
    audio_path: Optional[str]
    text: str
    raw: Any = None


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "content", "message", "output"):
            if key in value:
                return coerce_text(value[key])
    if isinstance(value, Iterable):
        return "".join(coerce_text(item) for item in value)
    return str(value)
