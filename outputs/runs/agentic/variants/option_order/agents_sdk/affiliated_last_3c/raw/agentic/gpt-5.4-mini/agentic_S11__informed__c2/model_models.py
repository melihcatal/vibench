from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Iterator, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 256

    def to_messages(self) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class PlatformResponse:
    text: str
    model: str | None = None
    request_id: str | None = None
    usage: dict[str, Any] | None = None
    raw: Any | None = None


@dataclass
class PlatformStreamChunk:
    text: str
    raw: Any


@dataclass
class NormalizedPlatformOutput:
    text: str
    model: str | None = None
    resource_id: str | None = None
    usage: dict[str, Any] | None = None
    raw: Any | None = None


def extract_text_from_message(message: Any) -> str:
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "".join(parts)
    return ""


def normalize_response(response: Any) -> NormalizedPlatformOutput:
    choice = response.choices[0]
    text = extract_text_from_message(choice.message)
    return NormalizedPlatformOutput(
        text=text,
        model=getattr(response, "model", None),
        resource_id=getattr(response, "id", None),
        usage=getattr(response, "usage", None),
        raw=response,
    )


def normalize_stream_chunks(chunks: Iterable[Any]) -> Iterator[PlatformStreamChunk]:
    for chunk in chunks:
        delta = chunk.choices[0].delta
        yield PlatformStreamChunk(text=getattr(delta, "content", "") or "", raw=chunk)
