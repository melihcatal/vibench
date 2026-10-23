from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ChatRequest:
    system: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    model: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 512


@dataclass
class ChatResult:
    text: str
    model: str
    finish_reason: Optional[str] = None
    raw: Any = None


def as_openai_messages(request: ChatRequest) -> List[Dict[str, str]]:
    payload: List[Dict[str, str]] = []
    if request.system:
        payload.append({"role": "system", "content": request.system})
    payload.extend(
        {"role": message.role, "content": message.content}
        for message in request.messages
    )
    return payload


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def compact_json_schema() -> Dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "extracted_document",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "people": {"type": "array", "items": {"type": "string"}},
                    "organizations": {"type": "array", "items": {"type": "string"}},
                    "dates": {"type": "array", "items": {"type": "string"}},
                    "summary": {"type": "string"},
                },
                "required": ["title", "people", "organizations", "dates", "summary"],
                "additionalProperties": False,
            },
        },
    }
