from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatRequest:
    system_prompt: str
    user_prompt: str
    model: str
    temperature: float = 0.2
    max_output_tokens: int = 500

    def to_openai_messages(self) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt},
        ]


@dataclass
class ChatResult:
    text: str
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)
    finish_reason: Optional[str] = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, Any]
    model: str


def extract_text_from_response(response: Any) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text
    if hasattr(response, "choices") and response.choices:
        message = getattr(response.choices[0], "message", None)
        if message and getattr(message, "content", None):
            content = message.content
            if isinstance(content, str):
                return content
        delta = getattr(response.choices[0], "delta", None)
        if delta and getattr(delta, "content", None):
            return delta.content
    return ""


def usage_to_dict(response: Any) -> Dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    if isinstance(usage, dict):
        return usage
    return {
        key: getattr(usage, key)
        for key in dir(usage)
        if not key.startswith("_") and not callable(getattr(usage, key))
    }
