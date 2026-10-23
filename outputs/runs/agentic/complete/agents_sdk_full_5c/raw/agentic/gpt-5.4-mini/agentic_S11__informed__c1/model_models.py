from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class PromptRequest:
    messages: List[Dict[str, str]]
    temperature: float = 0.2
    max_tokens: int = 256


@dataclass(frozen=True)
class PlatformResponse:
    text: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    resource_id: Optional[str] = None
    response_id: Optional[str] = None


@dataclass(frozen=True)
class StreamChunk:
    text: str
    raw: Any


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def extract_message_text(response: Any) -> str:
    try:
        return response.choices[0].message.content or ""
    except Exception:
        return normalize_text(response)


def extract_stream_text(chunk: Any) -> str:
    try:
        return chunk.choices[0].delta.content or ""
    except Exception:
        return ""
