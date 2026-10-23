from __future__ import annotations

import os
from typing import Iterable, Iterator, Optional

from openai import OpenAI

from model_models import EmbeddingResult, GenerationRequest, GenerationResult

DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "omni-moderation-latest")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def pick_model(explicit_model: Optional[str] = None, *, family: str = "chat") -> str:
    if explicit_model:
        return explicit_model
    if family == "embedding":
        return DEFAULT_EMBEDDING_MODEL
    if family == "safety":
        return DEFAULT_SAFETY_MODEL
    if family == "tts":
        return DEFAULT_TTS_MODEL
    return DEFAULT_CHAT_MODEL


def create_chat_completion(request: GenerationRequest) -> GenerationResult:
    client = get_openai_client()
    model = pick_model(request.model, family="chat")
    response = client.chat.completions.create(
        model=model,
        messages=request.normalized_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    choice = response.choices[0]
    usage = response.usage.model_dump() if response.usage else {}
    return GenerationResult(
        text=choice.message.content or "",
        model=response.model,
        finish_reason=choice.finish_reason,
        usage=usage,
    )


def stream_chat_completion(request: GenerationRequest) -> Iterator[str]:
    client = get_openai_client()
    model = pick_model(request.model, family="chat")
    stream = client.chat.completions.create(
        model=model,
        messages=request.normalized_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def create_embedding(text: str, model: Optional[str] = None) -> EmbeddingResult:
    client = get_openai_client()
    embedding_model = pick_model(model, family="embedding")
    response = client.embeddings.create(model=embedding_model, input=text)
    usage = response.usage.model_dump() if response.usage else {}
    return EmbeddingResult(
        vector=response.data[0].embedding,
        model=response.model,
        usage=usage,
    )


def collect_stream(chunks: Iterable[str]) -> str:
    return "".join(chunks)
