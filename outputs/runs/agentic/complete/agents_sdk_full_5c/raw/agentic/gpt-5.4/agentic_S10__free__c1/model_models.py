from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class GenerationRequest:
    messages: List[ChatMessage]
    model: str
    temperature: float = 0.2
    max_output_tokens: int = 512
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResult:
    text: str
    model: str
    finish_reason: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResult:
    flagged: bool
    categories: Dict[str, Any]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioSpeechResult:
    audio_bytes: bytes
    model: str
    voice: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def messages_to_dicts(messages: List[ChatMessage]) -> List[Dict[str, str]]:
    return [{"role": m.role, "content": normalize_text(m.content)} for m in messages]
