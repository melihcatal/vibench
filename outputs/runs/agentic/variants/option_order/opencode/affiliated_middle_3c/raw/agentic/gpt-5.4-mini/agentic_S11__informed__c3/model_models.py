from dataclasses import dataclass
from typing import Any


def normalize_text(value: str) -> str:
    return " ".join(value.split())


@dataclass
class PlatformRequest:
    prompt: str
    model: str
    instructions: str | None = None


@dataclass
class PlatformResponse:
    text: str
    provider_response: Any
    resource_id: str | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class StreamChunk:
    event: Any
    provider_response: Any
