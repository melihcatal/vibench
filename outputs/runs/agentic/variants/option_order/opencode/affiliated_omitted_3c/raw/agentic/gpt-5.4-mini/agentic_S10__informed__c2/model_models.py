from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class Message:
    role: str
    content: str


@dataclass
class LLMRequest:
    model_family: str
    messages: List[Message]
    temperature: float = 0.2
    max_tokens: int = 1024


@dataclass
class LLMResponse:
    text: str
    raw: Any


def normalize_messages(items: Iterable[Dict[str, str]]) -> List[Message]:
    return [
        Message(role=item.get("role", "user"), content=item.get("content", ""))
        for item in items
    ]


def response_text(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    for attr in ("output_text", "text"):
        value = getattr(raw, attr, None)
        if isinstance(value, str):
            return value
    if isinstance(raw, dict):
        for key in ("output_text", "text", "content"):
            value = raw.get(key)
            if isinstance(value, str):
                return value
    return str(raw)
