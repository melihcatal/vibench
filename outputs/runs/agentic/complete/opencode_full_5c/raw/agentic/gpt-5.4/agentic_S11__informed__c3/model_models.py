from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Iterator, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.2
    top_p: float = 0.95
    locale: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_messages(self) -> List[Dict[str, str]]:
        return [{"role": "user", "content": self.prompt}]


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource: str
    usage: Dict[str, Any] = field(default_factory=dict)
    provider_response: Any = None


def normalize_content(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: List[str] = []
        for item in value:
            if isinstance(item, dict):
                text = item.get("text") or item.get("content") or ""
                if text:
                    parts.append(str(text))
            else:
                parts.append(str(item))
        return "".join(parts)
    return str(value)


def collect_stream_text(events: Iterable[Any]) -> str:
    chunks: List[str] = []
    for event in events:
        delta = getattr(event, "delta", None)
        if delta and getattr(delta, "content", None):
            chunks.append(normalize_content(delta.content))
            continue
        choices = getattr(event, "choices", None)
        if choices:
            for choice in choices:
                choice_delta = getattr(choice, "delta", None)
                if choice_delta and getattr(choice_delta, "content", None):
                    chunks.append(normalize_content(choice_delta.content))
        elif isinstance(event, dict):
            for choice in event.get("choices", []):
                delta_dict = choice.get("delta", {})
                if delta_dict.get("content"):
                    chunks.append(normalize_content(delta_dict["content"]))
    return "".join(chunks)


def iter_stream_objects(events: Iterable[Any]) -> Iterator[Any]:
    for event in events:
        yield event
