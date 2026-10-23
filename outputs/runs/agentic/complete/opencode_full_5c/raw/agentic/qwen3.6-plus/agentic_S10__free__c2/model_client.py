from __future__ import annotations

import os
from typing import Any, Generator, Optional

from openai import OpenAI

from model_models import (
    EmbeddingResponse,
    LLMRequest,
    LLMResponse,
    SpokenBriefResponse,
    StreamChunk,
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "gpt-4o")
DEFAULT_EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.environ.get("TTS_MODEL", "tts-1")
DEFAULT_VOICE = os.environ.get("TTS_VOICE", "alloy")


_client: Optional[OpenAI] = None


def get_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=api_key or OPENAI_API_KEY,
            base_url=base_url or OPENAI_BASE_URL,
        )
    return _client


def reset_client() -> None:
    global _client
    _client = None


def build_messages(
    prompt: str,
    system_prompt: Optional[str] = None,
) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


def call_llm(
    request: LLMRequest,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    client = get_client(api_key, base_url)
    payload = request.to_openai_payload()
    response = client.chat.completions.create(**payload)
    return LLMResponse.from_openai(response)


def stream_llm(
    request: LLMRequest,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Generator[StreamChunk, None, None]:
    client = get_client(api_key, base_url)
    request.stream = True
    payload = request.to_openai_payload()
    stream = client.chat.completions.create(**payload)
    for chunk in stream:
        if not chunk.choices:
            continue
        choice = chunk.choices[0]
        delta = choice.delta
        yield StreamChunk(
            delta=delta.content or "",
            index=choice.index,
            finish_reason=choice.finish_reason,
            model_used=chunk.model,
        )


def create_embedding(
    text: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> EmbeddingResponse:
    client = get_client(api_key, base_url)
    response = client.embeddings.create(
        model=model or DEFAULT_EMBEDDING_MODEL,
        input=text,
    )
    return EmbeddingResponse.from_openai(response)


def create_speech(
    text: str,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> SpokenBriefResponse:
    client = get_client(api_key, base_url)
    response = client.audio.speech.create(
        model=model or DEFAULT_TTS_MODEL,
        voice=voice or DEFAULT_VOICE,
        input=text,
        response_format="mp3",
    )
    return SpokenBriefResponse(
        text=text,
        audio_url=None,
        model_used=model or DEFAULT_TTS_MODEL,
        voice=voice or DEFAULT_VOICE,
        raw={"content_length": len(response.content)},
    )


def create_moderation(
    text: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> dict[str, Any]:
    client = get_client(api_key, base_url)
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
