from __future__ import annotations

import os
from typing import Iterator

from openai import OpenAI

from model_models import ChatRequest, ChatResult, EmbeddingResult, SafetyResult, normalize_text

DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
DEFAULT_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
DEFAULT_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def run_chat(request: ChatRequest) -> ChatResult:
    client = get_openai_client()
    response = client.responses.create(
        model=request.model,
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
        input=request.to_messages(),
    )
    return ChatResult(
        text=normalize_text(response.output_text),
        model=request.model,
        raw=response,
    )


def stream_chat(request: ChatRequest) -> Iterator[str]:
    client = get_openai_client()
    with client.responses.stream(
        model=request.model,
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
        input=request.to_messages(),
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta
        stream.get_final_response()


def create_embedding(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=normalize_text(text),
    )
    item = response.data[0]
    return EmbeddingResult(vector=item.embedding, model=model, raw=response)


def moderate_text(text: str) -> SafetyResult:
    client = get_openai_client()
    response = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=normalize_text(text),
    )
    result = response.results[0]
    categories = {name: bool(value) for name, value in result.categories.model_dump().items()}
    return SafetyResult(flagged=bool(result.flagged), categories=categories, raw=response)
