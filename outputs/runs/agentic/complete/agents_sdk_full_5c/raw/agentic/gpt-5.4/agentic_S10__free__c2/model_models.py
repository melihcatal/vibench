from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatRequest:
    system_prompt: str
    user_prompt: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 400

    def to_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.user_prompt})
        return messages


@dataclass
class ChatResult:
    text: str
    model: str
    provider: str = "openai"
    raw: Optional[Any] = None


@dataclass
class EmbeddingResult:
    vector: List[float] = field(default_factory=list)
    model: str = "text-embedding-3-large"
    provider: str = "openai"
    raw: Optional[Any] = None


@dataclass
class SafetyResult:
    flagged: bool
    categories: Dict[str, bool]
    provider: str = "openai"
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def compact_json_schema() -> Dict[str, Any]:
    return {
        "name": "extracted_record",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "people": {"type": "array", "items": {"type": "string"}},
                "organizations": {"type": "array", "items": {"type": "string"}},
                "dates": {"type": "array", "items": {"type": "string"}},
                "summary": {"type": "string"},
            },
            "required": ["people", "organizations", "dates", "summary"],
        },
        "strict": True,
    }
