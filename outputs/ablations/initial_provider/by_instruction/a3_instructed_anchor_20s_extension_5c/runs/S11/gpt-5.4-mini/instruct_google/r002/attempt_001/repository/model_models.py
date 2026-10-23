from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    locale: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    model: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "output_text", "content"):
            if key in value and value[key] is not None:
                return normalize_text(value[key])
    if isinstance(value, list):
        return "\n".join(normalize_text(item) for item in value if normalize_text(item))
    return str(value).strip()


def to_response(text: Any, **kwargs: Any) -> PlatformResponse:
    return PlatformResponse(text=normalize_text(text), **kwargs)
