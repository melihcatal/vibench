from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model_id: Optional[str] = None
    max_tokens: int = 256
    temperature: float = 0.2


@dataclass
class PlatformResponse:
    text: str
    raw: Any
    usage: Optional[Dict[str, Any]] = None
    model_id: Optional[str] = None
    resource_id: Optional[str] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        for key in ("text", "content", "output_text", "result"):
            if key in value:
                return normalize_text(value[key])
    return str(value)
