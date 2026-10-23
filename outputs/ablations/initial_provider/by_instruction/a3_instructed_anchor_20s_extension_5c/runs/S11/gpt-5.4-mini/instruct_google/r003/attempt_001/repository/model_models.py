from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass
class PlatformRequest:
    prompt: str
    resource: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    metadata: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if hasattr(value, "text"):
        return str(value.text)
    if isinstance(value, Iterable):
        return "".join(str(item) for item in value)
    return str(value)
