from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlatformRequest:
    prompt: str = ""
    messages: list[dict[str, str]] = field(default_factory=list)
    temperature: float = 0.2
    max_tokens: int | None = None


@dataclass
class PlatformResource:
    provider: str
    resource_id: str
    model_id: str


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_id: str
    usage: Any = None
    raw_response: Any = None
