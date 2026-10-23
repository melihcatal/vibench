import os
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class ModelFamily(Enum):
    GPT4O = "gpt-4o"
    GPT4O_MINI = "gpt-4o-mini"
    GPT4_TURBO = "gpt-4-turbo"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TTS_1 = "tts-1"
    TTS_1_HD = "tts-1-hd"


@dataclass
class LLMRequest:
    model: str = ModelFamily.GPT4O_MINI.value
    messages: list[dict[str, str]] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    stream: bool = False
    response_format: Optional[dict[str, str]] = None
    stop: Optional[list[str]] = None


@dataclass
class LLMResponse:
    content: str
    model: str
    usage: dict[str, int] = field(default_factory=dict)
    finish_reason: Optional[str] = None


@dataclass
class StreamChunk:
    delta: str
    index: int
    finish_reason: Optional[str] = None


@dataclass
class EmbeddingRequest:
    model: str = ModelFamily.TEXT_EMBEDDING_3_SMALL.value
    input: str | list[str] = ""
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class EmbeddingResponse:
    embeddings: list[list[float]]
    model: str
    usage: dict[str, int] = field(default_factory=dict)


@dataclass
class ModerationRequest:
    input: str | list[str] = ""
    model: str = "omni-moderation-latest"


@dataclass
class ModerationResult:
    flagged: bool
    categories: dict[str, bool] = field(default_factory=dict)
    category_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class ModerationResponse:
    results: list[ModerationResult]
    model: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str = "en"
    source_language: Optional[str] = None
    model: str = ModelFamily.GPT4O_MINI.value


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source: str
    model: str


@dataclass
class TTSRequest:
    input_text: str
    model: str = ModelFamily.TTS_1.value
    voice: str = "alloy"
    response_format: str = "mp3"
    speed: float = 1.0


@dataclass
class SpokenBriefRequest:
    text: str
    target_length_seconds: int = 30
    voice: str = "alloy"
    model: str = ModelFamily.GPT4O_MINI.value
    tts_model: str = ModelFamily.TTS_1.value


@dataclass
class SpokenBriefResponse:
    audio_data: bytes
    brief_text: str
    audio_format: str = "mp3"


def normalize_messages(
    system_prompt: str,
    user_content: str,
    context: Optional[str] = None,
) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": system_prompt}]
    if context:
        messages.append(
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {user_content}"}
        )
    else:
        messages.append({"role": "user", "content": user_content})
    return messages


def extract_text_from_response(response: Any) -> str:
    if hasattr(response, "choices") and response.choices:
        return response.choices[0].message.content or ""
    if isinstance(response, dict) and "choices" in response:
        return response["choices"][0].get("message", {}).get("content", "")
    return str(response)


def parse_stream_chunk(chunk: Any) -> Optional[StreamChunk]:
    if hasattr(chunk, "choices") and chunk.choices:
        choice = chunk.choices[0]
        delta = choice.delta
        text = delta.content if hasattr(delta, "content") else ""
        return StreamChunk(
            delta=text or "",
            index=choice.index,
            finish_reason=choice.finish_reason,
        )
    return None


def build_completion_payload(request: LLMRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": request.model,
        "messages": request.messages,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "stream": request.stream,
    }
    if request.max_tokens is not None:
        payload["max_tokens"] = request.max_tokens
    if request.response_format is not None:
        payload["response_format"] = request.response_format
    if request.stop is not None:
        payload["stop"] = request.stop
    return payload


def build_embedding_payload(request: EmbeddingRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": request.model,
        "input": request.input,
        "encoding_format": request.encoding_format,
    }
    if request.dimensions is not None:
        payload["dimensions"] = request.dimensions
    return payload
