from __future__ import annotations

import os
from typing import Iterator

from openai import OpenAI

from model_models import ChatRequest, ChatResult, as_openai_messages, normalize_text


DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def choose_chat_model(task: str) -> str:
    mapping = {
        "summarize": os.getenv("OPENAI_SUMMARIZE_MODEL", DEFAULT_CHAT_MODEL),
        "extract": os.getenv("OPENAI_EXTRACT_MODEL", "gpt-4.1"),
        "qa": os.getenv("OPENAI_QA_MODEL", DEFAULT_CHAT_MODEL),
        "stream": os.getenv("OPENAI_STREAM_MODEL", DEFAULT_CHAT_MODEL),
    }
    return mapping.get(task, DEFAULT_CHAT_MODEL)


def complete_chat(request: ChatRequest) -> ChatResult:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=request.model or DEFAULT_CHAT_MODEL,
        messages=as_openai_messages(request),
        temperature=request.temperature,
        max_completion_tokens=request.max_output_tokens,
    )
    choice = response.choices[0]
    text = normalize_text(choice.message.content)
    return ChatResult(
        text=text,
        model=response.model,
        finish_reason=choice.finish_reason,
        raw=response,
    )


def stream_chat(request: ChatRequest) -> Iterator[str]:
    client = get_openai_client()
    stream = client.chat.completions.create(
        model=request.model or DEFAULT_CHAT_MODEL,
        messages=as_openai_messages(request),
        temperature=request.temperature,
        max_completion_tokens=request.max_output_tokens,
        stream=True,
    )
    for chunk in stream:
        for choice in chunk.choices:
            delta = getattr(choice.delta, "content", None)
            if delta:
                yield delta
