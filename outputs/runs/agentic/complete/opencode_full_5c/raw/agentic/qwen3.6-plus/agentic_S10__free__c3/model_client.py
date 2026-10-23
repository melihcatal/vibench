from __future__ import annotations

import os
from typing import Any, Dict, Generator, List, Optional

from openai import OpenAI

from model_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    LLMRequest,
    LLMResponse,
    ModerationRequest,
    ModerationResponse,
    SpeechRequest,
    SpeechResponse,
    StreamChunk,
    TranslationRequest,
    TranslationResponse,
    normalize_completion_response,
    normalize_embedding_response,
    normalize_moderation_response,
    normalize_stream_chunk,
    normalize_translation_response,
)

OPENAI_API_BASE = "https://api.openai.com/v1"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(
        api_key=api_key,
        base_url=OPENAI_API_BASE,
    )


def load_model_config() -> Dict[str, Any]:
    return {
        "default_model": os.environ.get("LLM_DEFAULT_MODEL", "gpt-4o-2024-08-06"),
        "embedding_model": os.environ.get(
            "LLM_EMBEDDING_MODEL", "text-embedding-3-small"
        ),
        "tts_model": os.environ.get("LLM_TTS_MODEL", "tts-1"),
        "moderation_model": os.environ.get(
            "LLM_MODERATION_MODEL", "omni-moderation-latest"
        ),
        "default_temperature": float(os.environ.get("LLM_DEFAULT_TEMPERATURE", "0.7")),
        "default_max_tokens": int(os.environ.get("LLM_DEFAULT_MAX_TOKENS", "4096")),
        "api_base": OPENAI_API_BASE,
    }


def build_completion_payload(request: LLMRequest) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
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


def create_completion(request: LLMRequest) -> LLMResponse:
    client = get_openai_client()
    payload = build_completion_payload(request)
    raw = client.chat.completions.create(**payload)
    return normalize_completion_response(raw.model_dump())


def create_stream_completion(request: LLMRequest) -> Generator[StreamChunk, None, None]:
    client = get_openai_client()
    payload = build_completion_payload(request)
    payload["stream"] = True
    stream = client.chat.completions.create(**payload)
    for chunk in stream:
        yield normalize_stream_chunk(chunk.model_dump())


def create_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    client = get_openai_client()
    payload: Dict[str, Any] = {
        "model": request.model,
        "input": request.input_text,
        "encoding_format": request.encoding_format,
    }
    if request.dimensions is not None:
        payload["dimensions"] = request.dimensions
    raw = client.embeddings.create(**payload)
    return normalize_embedding_response(raw.model_dump())


def create_moderation(request: ModerationRequest) -> ModerationResponse:
    client = get_openai_client()
    raw = client.moderations.create(
        model=request.model,
        input=request.input_text,
    )
    return normalize_moderation_response(raw.model_dump())


def create_speech(request: SpeechRequest) -> SpeechResponse:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=request.model,
        voice=request.voice,
        input=request.input_text,
        response_format=request.response_format,
        speed=request.speed,
    )
    audio_bytes = response.content
    return SpeechResponse(
        audio_bytes=audio_bytes,
        model=request.model,
        content_type="audio/mpeg"
        if request.response_format == "mp3"
        else f"audio/{request.response_format}",
        raw_response=response,
    )


def create_translation(request: TranslationRequest) -> TranslationResponse:
    client = get_openai_client()
    system_parts: List[str] = [
        "You are a professional translator.",
        f"Translate the following text to {request.target_language}.",
    ]
    if request.source_language:
        system_parts.append(f"The source language is {request.source_language}.")
    system_parts.append(
        "Return only the translated text with no additional commentary."
    )

    messages = [
        {"role": "system", "content": " ".join(system_parts)},
        {"role": "user", "content": request.source_text},
    ]
    raw = client.chat.completions.create(
        model=request.model,
        messages=messages,
        temperature=request.temperature,
    )
    return normalize_translation_response(raw.model_dump())
