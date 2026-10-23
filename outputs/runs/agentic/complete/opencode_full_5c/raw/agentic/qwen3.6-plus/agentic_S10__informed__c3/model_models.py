import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LLMRequest:
    prompt: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1024
    system_prompt: Optional[str] = None
    json_mode: bool = False


@dataclass
class LLMResponse:
    text: str
    model: str
    finish_reason: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class StreamChunk:
    text: str
    index: int
    finish_reason: Optional[str] = None


@dataclass
class SafetyResult:
    is_safe: bool
    scores: dict
    flagged_attributes: list = field(default_factory=list)


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class EmbeddingResult:
    embedding: list
    model: str
    dimensions: int


@dataclass
class SpeechResult:
    audio_data: bytes
    format: str
    duration_seconds: Optional[float] = None


def normalize_openai_response(raw_response) -> LLMResponse:
    choice = raw_response.choices[0]
    usage = raw_response.usage
    return LLMResponse(
        text=choice.message.content or "",
        model=raw_response.model,
        finish_reason=choice.finish_reason or "unknown",
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
    )


def normalize_stream_chunk(raw_chunk) -> Optional[StreamChunk]:
    if not raw_chunk.choices:
        return None
    choice = raw_chunk.choices[0]
    delta = choice.delta
    text = delta.content if delta and delta.content else ""
    if not text and not choice.finish_reason:
        return None
    return StreamChunk(
        text=text or "",
        index=choice.index,
        finish_reason=choice.finish_reason,
    )


def build_messages(system_prompt: Optional[str], user_prompt: str) -> list:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    return messages
