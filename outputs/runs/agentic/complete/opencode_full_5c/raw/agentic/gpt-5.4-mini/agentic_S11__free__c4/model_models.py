from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model: Optional[str] = None
    deployment: Optional[str] = None
    stream: bool = False
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class PlatformResponse:
    text: str
    model: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "content", "output", "message"):
            if key in value:
                return normalize_text(value[key])
    if isinstance(value, list):
        return "".join(normalize_text(item) for item in value)
    return str(value).strip()
