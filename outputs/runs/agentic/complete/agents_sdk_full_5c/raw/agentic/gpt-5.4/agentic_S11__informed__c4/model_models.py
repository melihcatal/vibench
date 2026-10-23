from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ModelInvocationRequest:
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 512
    system_instruction: Optional[str] = None
    deployment_name: Optional[str] = None
    model: Optional[str] = None
    extra_body: Dict[str, Any] = field(default_factory=dict)

    def to_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system_instruction:
            messages.append({"role": "system", "content": self.system_instruction})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class NormalizedModelResult:
    text: str
    model: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    provider_response_id: Optional[str] = None
    resource_name: Optional[str] = None
    finish_reason: Optional[str] = None
    raw: Any = None


@dataclass
class StreamChunk:
    text_delta: str
    raw_chunk: Any


def collect_text_from_choices(choices: Iterable[Any]) -> str:
    parts: List[str] = []
    for choice in choices or []:
        message = getattr(choice, "message", None)
        if message is not None:
            content = getattr(message, "content", None)
            if content:
                parts.append(str(content))
                continue
        delta = getattr(choice, "delta", None)
        if delta is not None:
            content = getattr(delta, "content", None)
            if content:
                parts.append(str(content))
                continue
        text = getattr(choice, "text", None)
        if text:
            parts.append(str(text))
    return "".join(parts)


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return dict(usage)
    result: Dict[str, Any] = {}
    for field_name in ("prompt_tokens", "completion_tokens", "total_tokens", "input_tokens", "output_tokens"):
        value = getattr(usage, field_name, None)
        if value is not None:
            result[field_name] = value
    if hasattr(usage, "model_dump"):
        result.update(usage.model_dump())
    return result
