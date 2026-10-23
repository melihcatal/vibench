from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LLMMessage:
    role: str
    content: str


@dataclass
class LLMResponse:
    text: str
    raw: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def messages_to_contents(messages: List[LLMMessage]) -> List[Dict[str, Any]]:
    return [{"role": m.role, "parts": [{"text": m.content}]} for m in messages]


def extract_text_from_response(data: Dict[str, Any]) -> str:
    candidates = data.get("candidates", []) or []
    if not candidates:
        return ""
    content = candidates[0].get("content", {}) or {}
    parts = content.get("parts", []) or []
    return "".join(part.get("text", "") for part in parts).strip()
