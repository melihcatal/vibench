from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 256


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Optional[Any] = None


def extract_text(response: Any) -> str:
    if hasattr(response, "choices") and response.choices:
        choice = response.choices[0]
        if hasattr(choice, "message") and choice.message:
            return getattr(choice.message, "content", "") or ""
        if hasattr(choice, "text"):
            return getattr(choice, "text", "") or ""
    return str(response)


def response_usage(response: Any) -> Optional[Dict[str, Any]]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    return dict(usage)


def stream_text(chunks: Iterable[Any]) -> str:
    parts: List[str] = []
    for chunk in chunks:
        delta = None
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0]
            if hasattr(delta, "delta") and delta.delta:
                parts.append(getattr(delta.delta, "content", "") or "")
            elif hasattr(delta, "text"):
                parts.append(getattr(delta, "text", "") or "")
        else:
            parts.append(str(chunk))
    return "".join(parts)
