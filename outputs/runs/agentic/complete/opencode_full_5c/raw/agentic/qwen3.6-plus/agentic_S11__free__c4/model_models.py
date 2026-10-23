from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional, Sequence


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class PlatformMessage:
    role: MessageRole
    content: str


@dataclass
class PlatformRequest:
    messages: list[PlatformMessage]
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    stop: Optional[list[str]] = None
    stream: bool = False
    seed: Optional[int] = None
    extra_body: dict[str, Any] = field(default_factory=dict)

    def to_openai_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": m.role.value, "content": m.content} for m in self.messages
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": self.stream,
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.stop is not None:
            payload["stop"] = self.stop
        if self.seed is not None:
            payload["seed"] = self.seed
        if self.extra_body:
            payload.update(self.extra_body)
        return payload


@dataclass
class PlatformUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw: Optional[Mapping[str, Any]] = None


@dataclass
class PlatformMetadata:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    model: str = ""
    model_id: str = ""
    provider: str = "openai"
    usage: Optional[PlatformUsage] = None
    system_fingerprint: Optional[str] = None
    created: Optional[int] = None
    raw_response: Optional[Any] = None


@dataclass
class PlatformResponse:
    content: str
    finish_reason: Optional[str] = None
    metadata: PlatformMetadata = field(default_factory=PlatformMetadata)
    raw: Optional[Any] = None


@dataclass
class StreamChunk:
    delta: str
    finish_reason: Optional[str] = None
    index: int = 0
    raw_chunk: Optional[Any] = None


@dataclass
class StreamedResponse:
    content: str
    chunks: list[StreamChunk] = field(default_factory=list)
    metadata: PlatformMetadata = field(default_factory=PlatformMetadata)
    raw_response: Optional[Any] = None


@dataclass
class SafetyResult:
    flagged: bool
    categories: dict[str, bool] = field(default_factory=dict)
    category_scores: dict[str, float] = field(default_factory=dict)
    raw: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embedding: list[float]
    model: str = ""
    usage: Optional[PlatformUsage] = None
    raw: Optional[Any] = None


@dataclass
class AudioResult:
    audio_data: bytes
    format: str = "mp3"
    model: str = ""
    usage: Optional[PlatformUsage] = None
    raw: Optional[Any] = None


def normalize_openai_response(raw_response: Any) -> PlatformResponse:
    choice = raw_response.choices[0]
    content = choice.message.content or ""
    usage_data = raw_response.usage
    usage = PlatformUsage(
        prompt_tokens=usage_data.prompt_tokens,
        completion_tokens=usage_data.completion_tokens,
        total_tokens=usage_data.total_tokens,
        raw=usage_data.model_dump() if hasattr(usage_data, "model_dump") else None,
    )
    metadata = PlatformMetadata(
        model=raw_response.model,
        model_id=raw_response.model,
        provider="openai",
        usage=usage,
        system_fingerprint=getattr(raw_response, "system_fingerprint", None),
        created=getattr(raw_response, "created", None),
        raw_response=raw_response,
    )
    return PlatformResponse(
        content=content,
        finish_reason=choice.finish_reason,
        metadata=metadata,
        raw=raw_response,
    )


def normalize_streamed_response(
    chunks: list[StreamChunk], raw_response: Any
) -> StreamedResponse:
    content = "".join(c.delta for c in chunks)
    metadata = PlatformMetadata(
        model=raw_response.model if hasattr(raw_response, "model") else "",
        model_id=raw_response.model if hasattr(raw_response, "model") else "",
        provider="openai",
        raw_response=raw_response,
    )
    return StreamedResponse(
        content=content,
        chunks=chunks,
        metadata=metadata,
        raw_response=raw_response,
    )
