from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str

    def as_openai(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class GenerationConfig:
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 400
    top_p: float = 1.0


@dataclass
class SummaryResult:
    summary: str
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JsonExtractionResult:
    data: Dict[str, Any]
    raw_text: str
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnswerResult:
    answer: str
    model: str
    citations: List[str] = field(default_factory=list)
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamChunk:
    text: str
    done: bool = False


@dataclass
class SafetyResult:
    provider: str
    unsafe: bool
    scores: Dict[str, Any] = field(default_factory=dict)
    flagged_segments: List[str] = field(default_factory=list)


@dataclass
class TranslationResult:
    text: str
    detected_source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = ""


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int


@dataclass
class SpokenBriefResult:
    provider: str
    voice: str
    audio_bytes: bytes
    content_type: str


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def trim_text(text: str, max_chars: int) -> str:
    normalized = text.strip()
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + "..."


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return usage
    result: Dict[str, Any] = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = getattr(usage, key, None)
        if value is not None:
            result[key] = value
    return result


def join_text_parts(parts: Iterable[str]) -> str:
    return "".join(part for part in parts if part)
