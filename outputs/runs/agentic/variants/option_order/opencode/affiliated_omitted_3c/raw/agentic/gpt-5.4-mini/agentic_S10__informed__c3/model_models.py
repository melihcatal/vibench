from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 1024


@dataclass
class ContextQuestionRequest:
    context: str
    question: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 1024


@dataclass
class JsonExtractionResult:
    data: Dict[str, Any]
    raw_text: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def message_text(response: Any) -> str:
    choices = getattr(response, "choices", None) or []
    if choices:
        msg = getattr(choices[0], "message", None)
        if msg is not None:
            content = getattr(msg, "content", None)
            if content is not None:
                return normalize_text(content)
    return normalize_text(response)
