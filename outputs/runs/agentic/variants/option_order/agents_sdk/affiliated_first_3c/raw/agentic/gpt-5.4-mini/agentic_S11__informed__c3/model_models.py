from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union


TextLike = Union[str, Mapping[str, Any], Sequence[Any]]


@dataclass
class RequestEnvelope:
    prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 512
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedResponse:
    text: str
    provider: str
    model: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResource:
    provider: str
    resource_id: str
    model: str
    client_hint: str = "azure-openai"


def normalize_text(value: TextLike) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for key in ("prompt", "input", "text", "content"):
            if key in value and value[key] is not None:
                return str(value[key])
        return str(dict(value))
    if isinstance(value, Sequence):
        parts: List[str] = []
        for item in value:
            parts.append(normalize_text(item))
        return "\n".join(p for p in parts if p)
    return str(value)


def envelope_from_prompt(prompt: TextLike, **kwargs: Any) -> RequestEnvelope:
    return RequestEnvelope(prompt=normalize_text(prompt), **kwargs)


def response_from_choice(text: str, provider: str, model: str, **metadata: Any) -> NormalizedResponse:
    return NormalizedResponse(text=text, provider=provider, model=model, metadata=dict(metadata))
