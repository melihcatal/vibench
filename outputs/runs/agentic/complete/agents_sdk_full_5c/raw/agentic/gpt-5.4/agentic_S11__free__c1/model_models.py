from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(slots=True)
class GenerationRequest:
    prompt: str
    system: str | None = None
    max_output_tokens: int = 256
    temperature: float = 0.2
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_messages(self) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass(slots=True)
class PlatformSelection:
    project_id: str
    location: str
    publisher_model: str
    endpoint: str | None = None

    @property
    def model_resource(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.publisher_model}"


@dataclass(slots=True)
class GenerationResult:
    text: str
    model: str
    usage: dict[str, Any] = field(default_factory=dict)
    resource: str | None = None
    raw: Any = None


@dataclass(slots=True)
class StreamChunk:
    text: str
    raw: Any



def coalesce_text(parts: Iterable[str | None]) -> str:
    return "".join(part for part in parts if part)



def normalize_usage(metadata: Any) -> dict[str, Any]:
    if metadata is None:
        return {}
    if hasattr(metadata, "to_dict"):
        return metadata.to_dict()
    if isinstance(metadata, dict):
        return metadata
    usage: dict[str, Any] = {}
    for attr in (
        "prompt_token_count",
        "candidates_token_count",
        "total_token_count",
        "traffic_type",
    ):
        if hasattr(metadata, attr):
            usage[attr] = getattr(metadata, attr)
    return usage
