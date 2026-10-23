from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str

    def to_openai(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class GenerationRequest:
    messages: List[ChatMessage]
    model: str
    temperature: float = 0.2
    max_output_tokens: Optional[int] = None

    def to_openai(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [message.to_openai() for message in self.messages],
            "temperature": self.temperature,
        }
        if self.max_output_tokens is not None:
            payload["max_completion_tokens"] = self.max_output_tokens
        return payload


@dataclass
class GenerationResult:
    text: str
    model: str
    finish_reason: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)


def coerce_messages(items: Iterable[Dict[str, Any] | ChatMessage]) -> List[ChatMessage]:
    normalized: List[ChatMessage] = []
    for item in items:
        if isinstance(item, ChatMessage):
            normalized.append(item)
        else:
            normalized.append(
                ChatMessage(role=str(item["role"]), content=str(item["content"]))
            )
    return normalized


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_generation_response(response: Any) -> GenerationResult:
    choice = response.choices[0]
    message = getattr(choice, "message", None)
    text = ""
    if message is not None:
        text = normalize_text(getattr(message, "content", ""))
    usage = getattr(response, "usage", None)
    return GenerationResult(
        text=text,
        model=getattr(response, "model", ""),
        finish_reason=getattr(choice, "finish_reason", None),
        usage=dict(usage) if usage else {},
    )


def normalize_embedding_response(response: Any) -> EmbeddingResult:
    item = response.data[0]
    usage = getattr(response, "usage", None)
    return EmbeddingResult(
        vector=list(getattr(item, "embedding", [])),
        model=getattr(response, "model", "text-embedding-3-large"),
        usage=dict(usage) if usage else {},
    )
