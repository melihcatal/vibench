from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ModelRequest:
    prompt: str
    model: Optional[str] = None
    resource_id: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 256


@dataclass
class ModelResult:
    text: str
    model: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: List[str] = []
        for item in value:
            parts.append(normalize_text(item))
        return "".join(parts)
    if isinstance(value, dict):
        for key in ("text", "content", "message", "output_text"):
            if key in value:
                return normalize_text(value[key])
    return str(value)


def extract_usage(payload: Any) -> Optional[Dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("usage", "meta", "metadata"):
            if key in payload and isinstance(payload[key], dict):
                return payload[key]
    return None
