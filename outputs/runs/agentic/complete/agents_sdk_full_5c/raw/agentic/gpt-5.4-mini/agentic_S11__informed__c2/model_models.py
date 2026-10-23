from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 256
    model: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    model: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResource:
    kind: str
    identifier: str
    provider: str = "azure-openai"


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_response_text(text: str) -> str:
    return normalize_text(text)


def response_from_choice(choice: Any, usage: Any = None, model: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> PlatformResponse:
    content = getattr(choice.message, "content", "") if hasattr(choice, "message") else str(choice)
    return PlatformResponse(
        text=normalize_response_text(content),
        model=model,
        usage=dict(usage) if usage is not None and hasattr(usage, "model_dump") else (usage if isinstance(usage, dict) else None),
        metadata=metadata or {},
    )
