from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class ChatTurn:
    role: str
    content: str

    def as_openai_message(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(slots=True)
class InferenceRequest:
    model: str
    messages: List[ChatTurn]
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_openai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [m.as_openai_message() for m in self.messages],
            "temperature": self.temperature,
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload


@dataclass(slots=True)
class NormalizedTextResult:
    text: str
    model: str
    provider: str = "openai"
    finish_reason: Optional[str] = None
    raw: Any = None


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    model: str
    provider: str = "openai"
    raw: Any = None


@dataclass(slots=True)
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    model: str
    provider: str = "openai"
    raw: Any = None


@dataclass(slots=True)
class AudioSpeechResult:
    audio_bytes: bytes
    model: str
    voice: str
    provider: str = "openai"


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()
