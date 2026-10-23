from __future__ import annotations

import os
from typing import Generator, Optional

from openai import OpenAI

from model_models import ChatRequest, ChatResponse, as_message_payload


DEFAULT_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")
DEFAULT_AUDIO_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_EMBED_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def resolve_text_model(preferred_model: Optional[str] = None) -> str:
    return preferred_model or DEFAULT_TEXT_MODEL


def create_chat_completion(request: ChatRequest) -> ChatResponse:
    client = get_openai_client()
    model = resolve_text_model(request.model)
    response = client.chat.completions.create(
        model=model,
        messages=as_message_payload(request.system_prompt, request.user_prompt),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    choice = response.choices[0]
    text = choice.message.content or ""
    return ChatResponse(
        text=text,
        model=response.model,
        provider="openai",
        finish_reason=choice.finish_reason,
    )


def stream_chat_completion(request: ChatRequest) -> Generator[str, None, None]:
    client = get_openai_client()
    model = resolve_text_model(request.model)
    stream = client.chat.completions.create(
        model=model,
        messages=as_message_payload(request.system_prompt, request.user_prompt),
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
