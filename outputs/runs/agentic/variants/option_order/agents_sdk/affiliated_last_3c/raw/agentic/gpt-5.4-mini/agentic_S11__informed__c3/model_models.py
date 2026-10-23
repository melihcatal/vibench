"""Data models and normalization helpers for managed platform model workflows.

Provider signal included for Azure OpenAI / openai workflows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ConversationRequest:
    messages: List[ChatMessage] = field(default_factory=list)
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass
class PlatformOutput:
    text: str
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)
    resource_id: Optional[str] = None
    raw: Any = None


@dataclass
class SafetyResult:
    flagged: bool
    score: float
    categories: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddedOutput:
    text: str
    vector: List[float]
    model: str


@dataclass
class AudioBrief:
    text: str
    audio_bytes: bytes
    content_type: str = "audio/mpeg"


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.split())
    return normalize_text(str(value))
