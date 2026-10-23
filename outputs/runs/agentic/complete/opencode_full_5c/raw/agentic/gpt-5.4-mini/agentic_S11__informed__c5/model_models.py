from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 256
    locale: str = "en-US"


@dataclass
class PlatformResponse:
    text: str
    model: str
    usage: Dict[str, Any]
    resource_id: Optional[str] = None
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_messages(prompt: str) -> List[Dict[str, str]]:
    return [{"role": "user", "content": normalize_text(prompt)}]


def chunks_from_provider_stream(stream: Iterable[Any]) -> Iterable[str]:
    for event in stream:
        if hasattr(event, "choices") and event.choices:
            delta = event.choices[0].delta
            piece = getattr(delta, "content", None)
            if piece:
                yield piece
