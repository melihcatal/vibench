from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model: Optional[str] = None
    deployment: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    raw: Any
    metadata: Dict[str, Any]


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


def collect_metadata(obj: Any, keys: List[str]) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {}
    for key in keys:
        if isinstance(obj, dict) and key in obj:
            metadata[key] = obj[key]
        elif hasattr(obj, key):
            metadata[key] = getattr(obj, key)
    return metadata
