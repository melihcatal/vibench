from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class PlatformRequest:
    prompt: str
    system: str = ""
    temperature: float = 0.2
    max_tokens: int = 256


@dataclass
class PlatformResponse:
    text: str
    provider_metadata: dict[str, Any]


def normalize_messages(request: PlatformRequest) -> list[dict[str, str]]:
    messages = []
    if request.system:
        messages.append({"role": "system", "content": request.system})
    messages.append({"role": "user", "content": request.prompt})
    return messages


def collect_text(parts: Iterable[Any]) -> str:
    return "".join(str(part) for part in parts)
