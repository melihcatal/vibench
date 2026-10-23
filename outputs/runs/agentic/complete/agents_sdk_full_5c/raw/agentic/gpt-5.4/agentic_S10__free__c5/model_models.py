from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class ChatMessage:
    role: str
    content: str

    def to_openai(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(slots=True)
class GenerationRequest:
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: Optional[int] = None

    def normalized_messages(self) -> List[Dict[str, str]]:
        return [message.to_openai() for message in self.messages]


@dataclass(slots=True)
class GenerationResult:
    text: str
    model: str
    finish_reason: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def join_context(context_parts: List[str]) -> str:
    return "\n\n".join(part.strip() for part in context_parts if part and part.strip())
