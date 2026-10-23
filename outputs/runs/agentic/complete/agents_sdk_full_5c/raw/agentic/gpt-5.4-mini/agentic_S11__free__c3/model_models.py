from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class PlatformRequest:
    prompt: str
    resource_id: Optional[str] = None
    temperature: float = 0.2


@dataclass(frozen=True)
class PlatformResponse:
    text: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    resource_id: Optional[str] = None
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        if "text" in value:
            return normalize_text(value["text"])
        if "content" in value:
            return normalize_text(value["content"])
    return str(value).strip()
