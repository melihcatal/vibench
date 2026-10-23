from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PromptRequest:
    text: str
    system: Optional[str] = None
    context: Optional[str] = None
    question: Optional[str] = None
    schema_hint: Optional[Dict[str, Any]] = None


@dataclass
class ModelResponse:
    model: str
    content: str
    raw: Any = None
    usage: Optional[Dict[str, Any]] = None


@dataclass
class NormalizedOutput:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(normalize_text(item) for item in value if item is not None).strip()
    if isinstance(value, dict):
        if "text" in value:
            return normalize_text(value["text"])
        if "content" in value:
            return normalize_text(value["content"])
    return str(value).strip()


def response_to_normalized(response: Any, model: str) -> NormalizedOutput:
    content = getattr(response, "choices", None)
    text = ""
    if content:
        first = content[0]
        message = getattr(first, "message", None)
        if message is not None:
            text = normalize_text(getattr(message, "content", ""))
        else:
            text = normalize_text(getattr(first, "text", ""))
    if not text:
        text = normalize_text(response)
    usage = getattr(response, "usage", None)
    return NormalizedOutput(text=text, metadata={"model": model, "usage": getattr(usage, "model_dump", lambda: usage)() if usage else None})
