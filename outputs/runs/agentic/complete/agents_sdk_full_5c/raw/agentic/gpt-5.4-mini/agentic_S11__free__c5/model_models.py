from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    input_text: str
    model: Optional[str] = None
    temperature: float = 0.2
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class PlatformResponse:
    text: str
    model: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    resource_id: Optional[str] = None
    raw_response: Optional[Any] = None


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return text.strip()
    return str(text).strip()


def normalize_messages(text: str) -> List[Dict[str, str]]:
    return [{"role": "user", "content": normalize_text(text)}]
