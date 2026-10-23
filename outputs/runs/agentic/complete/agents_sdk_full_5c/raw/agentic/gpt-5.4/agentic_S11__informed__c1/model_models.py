from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


@dataclass(slots=True)
class GenerationRequest:
    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.2
    max_tokens: int = 512
    top_p: float | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_messages(self) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass(slots=True)
class GenerationResult:
    text: str
    model: str | None = None
    resource_id: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)
    provider_response: Any = None


@dataclass(slots=True)
class ResourceSelection:
    deployment_name: str
    model: str
    endpoint: str
    api_version: str


def extract_text_from_chat_completion(response: Any) -> str:
    choices = getattr(response, "choices", None) or []
    if not choices:
        return ""
    first = choices[0]
    message = getattr(first, "message", None)
    if message is not None:
        content = getattr(message, "content", None)
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, Mapping):
                    text = item.get("text")
                    if text:
                        parts.append(str(text))
            return "".join(parts)
    text = getattr(first, "text", None)
    return text or ""


def extract_stream_text(chunk: Any) -> str:
    choices = getattr(chunk, "choices", None) or []
    if not choices:
        return ""
    delta = getattr(choices[0], "delta", None)
    if delta is None:
        return ""
    content = getattr(delta, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, Iterable):
        parts: list[str] = []
        for item in content:
            text = getattr(item, "text", None)
            if text:
                parts.append(str(text))
        return "".join(parts)
    return ""


def usage_to_dict(usage: Any) -> dict[str, Any]:
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        return dict(usage.model_dump())
    if isinstance(usage, Mapping):
        return dict(usage)
    output: dict[str, Any] = {}
    for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = getattr(usage, name, None)
        if value is not None:
            output[name] = value
    return output
