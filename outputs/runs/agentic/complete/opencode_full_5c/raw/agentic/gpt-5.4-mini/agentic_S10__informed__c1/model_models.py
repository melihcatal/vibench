from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ChatRequest:
    prompt: str
    context: Optional[str] = None
    system: Optional[str] = None
    max_tokens: int = 512
    temperature: float = 0.2
    model: Optional[str] = None


@dataclass
class ChatResponse:
    text: str
    raw: Any


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        if "text" in value:
            return normalize_text(value["text"])
        if "content" in value:
            return normalize_text(value["content"])
        return "".join(f"{k}:{normalize_text(v)}" for k, v in value.items())
    return str(value)


def extract_message_text(response: Any) -> str:
    if response is None:
        return ""
    if hasattr(response, "output_text"):
        return normalize_text(response.output_text)
    if hasattr(response, "choices") and response.choices:
        choice = response.choices[0]
        message = getattr(choice, "message", None)
        if message is not None and hasattr(message, "content"):
            return normalize_text(message.content)
        if hasattr(choice, "text"):
            return normalize_text(choice.text)
    return normalize_text(response)
