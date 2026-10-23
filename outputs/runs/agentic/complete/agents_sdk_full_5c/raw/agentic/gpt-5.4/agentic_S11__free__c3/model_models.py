from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(slots=True)
class ModelPrompt:
    system: str | None = None
    user: str = ""
    temperature: float = 0.2
    max_output_tokens: int = 256

    def to_messages(self) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.user})
        return messages


@dataclass(slots=True)
class PlatformResource:
    model_id: str
    deployment_name: str | None = None
    region: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class NormalizedGeneration:
    text: str
    model: str | None
    resource_id: str | None
    usage: dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass(slots=True)
class SafetyAssessment:
    flagged: bool
    categories: list[str] = field(default_factory=list)
    raw: Any = None


@dataclass(slots=True)
class LocalizedOutput:
    locale: str
    text: str
    raw: Any = None


@dataclass(slots=True)
class EmbeddingVector:
    model: str
    vector: list[float]
    dimensions: int
    raw: Any = None


@dataclass(slots=True)
class AudioBrief:
    format: str
    audio_bytes: bytes
    transcript: str | None = None
    raw: Any = None


def coalesce_text(parts: Iterable[str | None]) -> str:
    return "".join(part for part in parts if part)
