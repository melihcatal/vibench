from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model_name: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResponse:
    text: str
    model_id: Optional[str] = None
    request_id: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class StreamChunk:
    text: str
    raw: Any = None
    done: bool = False


@dataclass
class NormalizedOutput:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        for key in ("text", "content", "output", "generated_text"):
            if key in value:
                return normalize_text(value[key])
    return str(value)


def normalize_usage(raw_usage: Any) -> Dict[str, Any]:
    if raw_usage is None:
        return {}
    if isinstance(raw_usage, dict):
        return dict(raw_usage)
    return {"value": raw_usage}
