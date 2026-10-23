from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512
    top_p: Optional[float] = None

    def to_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_id: str
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


def first_text_from_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                value = item.get("text")
                if isinstance(value, str):
                    parts.append(value)
        return "".join(parts)
    return ""


def normalize_openai_response(response: Any, resource_id: str) -> PlatformResponse:
    output_text = ""
    if getattr(response, "output_text", None):
        output_text = response.output_text
    elif getattr(response, "choices", None):
        choice = response.choices[0]
        message = getattr(choice, "message", None)
        if message is not None:
            output_text = first_text_from_content(getattr(message, "content", ""))
    usage_obj = getattr(response, "usage", None)
    usage = (
        usage_obj.model_dump()
        if hasattr(usage_obj, "model_dump")
        else (usage_obj or {})
    )
    raw = response.model_dump() if hasattr(response, "model_dump") else {}
    return PlatformResponse(
        text=output_text,
        model=getattr(response, "model", resource_id),
        resource_id=resource_id,
        usage=usage,
        raw=raw,
    )


def stream_event_text(event: Any) -> str:
    event_type = getattr(event, "type", "")
    if event_type == "response.output_text.delta":
        return getattr(event, "delta", "") or ""
    if event_type == "response.output_text.done":
        return getattr(event, "text", "") or ""
    return ""


def flatten_texts(items: Iterable[str]) -> str:
    return "".join(part for part in items if part)
