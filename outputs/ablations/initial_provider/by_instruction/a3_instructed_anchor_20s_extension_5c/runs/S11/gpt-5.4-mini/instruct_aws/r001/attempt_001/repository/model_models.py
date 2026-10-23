from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PlatformRequest:
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.2
    model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"


@dataclass
class PlatformResponse:
    text: str
    model_id: str
    usage: Dict[str, Any]
    raw: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        for key in ("text", "content", "output_text", "message"):
            if key in value:
                return normalize_text(value[key])
    return str(value)


def merge_usage(*parts: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for part in parts:
        if part:
            merged.update(part)
    return merged
