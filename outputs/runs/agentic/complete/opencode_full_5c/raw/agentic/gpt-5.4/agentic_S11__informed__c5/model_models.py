from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class PlatformRequest:
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 512
    system: str | None = None

    def to_messages(self) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass(slots=True)
class PlatformResponse:
    text: str
    model: str
    resource_id: str
    usage: dict[str, int | None]
    raw: Any


def extract_text(message: Any) -> str:
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text_value = item.get("text")
                if text_value:
                    parts.append(str(text_value))
            else:
                text_value = getattr(item, "text", None)
                if text_value:
                    parts.append(str(text_value))
        return "".join(parts)
    return ""


def usage_to_dict(usage: Any) -> dict[str, int | None]:
    if usage is None:
        return {"input_tokens": None, "output_tokens": None, "total_tokens": None}
    return {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }
