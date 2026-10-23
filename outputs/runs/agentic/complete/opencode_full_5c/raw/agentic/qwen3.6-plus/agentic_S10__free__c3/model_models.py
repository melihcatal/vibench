from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LLMRequest:
    model: str = "gpt-4o-2024-08-06"
    messages: List[Dict[str, str]] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    stream: bool = False
    response_format: Optional[Dict[str, str]] = None
    stop: Optional[List[str]] = None


@dataclass
class LLMResponse:
    content: str
    model: str
    finish_reason: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class StreamChunk:
    delta: str
    finish_reason: Optional[str]
    index: int = 0


@dataclass
class EmbeddingRequest:
    model: str = "text-embedding-3-small"
    input_text: str = ""
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str
    prompt_tokens: int = 0
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ModerationRequest:
    input_text: str = ""
    model: str = "omni-moderation-latest"


@dataclass
class ModerationResponse:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    model: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranslationRequest:
    source_text: str = ""
    target_language: str = "en"
    source_language: Optional[str] = None
    model: str = "gpt-4o-2024-08-06"
    temperature: float = 0.3


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: str = ""
    model: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SpeechRequest:
    input_text: str = ""
    model: str = "tts-1"
    voice: str = "alloy"
    response_format: str = "mp3"
    speed: float = 1.0


@dataclass
class SpeechResponse:
    audio_bytes: bytes = b""
    model: str = ""
    content_type: str = "audio/mpeg"
    raw_response: Optional[Any] = None


def normalize_messages(
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    context: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history:
        messages.extend(history)
    if context and user_prompt:
        messages.append(
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {user_prompt}",
            }
        )
    elif user_prompt:
        messages.append({"role": "user", "content": user_prompt})
    return messages


def normalize_completion_response(raw: Dict[str, Any]) -> LLMResponse:
    choice = raw.get("choices", [{}])[0]
    message = choice.get("message", {})
    usage = raw.get("usage", {})
    return LLMResponse(
        content=message.get("content", ""),
        model=raw.get("model", ""),
        finish_reason=choice.get("finish_reason", ""),
        prompt_tokens=usage.get("prompt_tokens", 0),
        completion_tokens=usage.get("completion_tokens", 0),
        total_tokens=usage.get("total_tokens", 0),
        raw_response=raw,
    )


def normalize_stream_chunk(raw: Dict[str, Any]) -> StreamChunk:
    choice = raw.get("choices", [{}])[0]
    delta = choice.get("delta", {})
    return StreamChunk(
        delta=delta.get("content", ""),
        finish_reason=choice.get("finish_reason"),
        index=choice.get("index", 0),
    )


def normalize_embedding_response(raw: Dict[str, Any]) -> EmbeddingResponse:
    data = raw.get("data", [{}])[0]
    usage = raw.get("usage", {})
    return EmbeddingResponse(
        embedding=data.get("embedding", []),
        model=raw.get("model", ""),
        prompt_tokens=usage.get("prompt_tokens", 0),
        raw_response=raw,
    )


def normalize_moderation_response(raw: Dict[str, Any]) -> ModerationResponse:
    result = raw.get("results", [{}])[0]
    return ModerationResponse(
        flagged=result.get("flagged", False),
        categories=result.get("categories", {}),
        category_scores=result.get("category_scores", {}),
        model=raw.get("model", ""),
        raw_response=raw,
    )


def normalize_translation_response(raw: Dict[str, Any]) -> TranslationResponse:
    choice = raw.get("choices", [{}])[0]
    message = choice.get("message", {})
    return TranslationResponse(
        translated_text=message.get("content", ""),
        model=raw.get("model", ""),
        raw_response=raw,
    )
