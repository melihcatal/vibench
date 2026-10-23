from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ChatRequest:
    prompt: str
    context: Optional[str] = None
    system: Optional[str] = None
    temperature: float = 0.2


@dataclass
class ChatResponse:
    text: str
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return str(value).strip()
    return str(value).strip()


def normalize_json_text(text: str) -> Dict[str, Any]:
    import json

    return json.loads(text)
