import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 256
    stream: bool = False


@dataclass
class PlatformResponse:
    output: str
    resource_id: Optional[str] = None
    model_id: Optional[str] = None
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


def first_env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def normalize_usage(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return {k: payload.get(k) for k in payload.keys()}
    return {}


def stream_chunks(chunks: Iterable[Any]) -> List[str]:
    return [normalize_text(chunk) for chunk in chunks if normalize_text(chunk)]
