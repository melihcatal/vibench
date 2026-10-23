import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelRequest:
    prompt: str
    context: Optional[str] = None
    system_prompt: Optional[str] = None
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2048
    json_mode: bool = False
    stop_sequences: Optional[list[str]] = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


@dataclass
class ModelResponse:
    text: str
    model: str
    finish_reason: str = "stop"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    metadata: dict = field(default_factory=dict)


@dataclass
class StreamChunk:
    text: str
    finish_reason: Optional[str] = None
    index: int = 0


@dataclass
class EmbeddingResponse:
    embeddings: list[list[float]]
    model: str
    total_tokens: int = 0


@dataclass
class SafetyResponse:
    is_safe: bool
    categories: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str = "auto"
    target_language: str = "en"
    metadata: dict = field(default_factory=dict)


@dataclass
class SpeechResponse:
    audio_data: bytes
    content_type: str = "audio/mpeg"
    metadata: dict = field(default_factory=dict)


def normalize_system_prompt(request: ModelRequest, default: str = "") -> str:
    if request.system_prompt:
        return request.system_prompt
    return default


def build_messages(request: ModelRequest, default_system: str = "") -> list[dict]:
    messages = []
    system_content = normalize_system_prompt(request, default_system)
    if system_content:
        messages.append({"role": "system", "content": system_content})
    if request.context:
        messages.append({"role": "user", "content": f"Context:\n{request.context}"})
    messages.append({"role": "user", "content": request.prompt})
    return messages


def parse_openai_response(response) -> ModelResponse:
    choice = response.choices[0]
    return ModelResponse(
        text=choice.message.content or "",
        model=response.model,
        finish_reason=choice.finish_reason or "stop",
        prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
        completion_tokens=response.usage.completion_tokens if response.usage else 0,
        total_tokens=response.usage.total_tokens if response.usage else 0,
    )


def parse_openai_stream_chunk(chunk) -> Optional[StreamChunk]:
    if not chunk.choices:
        return None
    choice = chunk.choices[0]
    delta = choice.delta
    content = delta.content if delta else None
    if content is None and choice.finish_reason is None:
        return None
    return StreamChunk(
        text=content or "",
        finish_reason=choice.finish_reason,
        index=choice.index,
    )
