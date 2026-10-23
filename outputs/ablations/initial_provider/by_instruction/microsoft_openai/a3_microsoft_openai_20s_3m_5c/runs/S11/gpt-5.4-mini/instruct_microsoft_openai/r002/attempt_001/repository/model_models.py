from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 256


@dataclass
class PlatformResponse:
    text: str
    model: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    resource_id: Optional[str] = None


def normalize_text(parts: Iterable[Any]) -> str:
    values: List[str] = []
    for part in parts:
        text = getattr(part, "text", None)
        if text:
            values.append(text)
    return "".join(values)
