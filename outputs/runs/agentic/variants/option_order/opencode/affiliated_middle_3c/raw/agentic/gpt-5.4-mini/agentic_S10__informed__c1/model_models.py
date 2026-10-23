import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class LLMRequest:
    prompt: str
    context: Optional[str] = None
    model: Optional[str] = None


@dataclass
class LLMResponse:
    text: str
    model: Optional[str] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_json_text(text: str) -> Dict[str, Any]:
    return json.loads(text)
