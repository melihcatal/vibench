from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Iterator, Optional

from openai import OpenAI

from model_models import ChatMessage, GenerationRequest, coerce_messages


DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL", "gpt-4.1")
DEFAULT_AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
DEFAULT_MODERATION_MODEL = os.getenv(
    "OPENAI_MODERATION_MODEL", "omni-moderation-latest"
)
DEFAULT_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def build_chat_request(
    system_prompt: str,
    user_prompt: str,
    *,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: Optional[int] = None,
    extra_messages: Optional[Iterable[Dict[str, Any] | ChatMessage]] = None,
) -> GenerationRequest:
    messages = [ChatMessage(role="system", content=system_prompt)]
    if extra_messages:
        messages.extend(coerce_messages(extra_messages))
    messages.append(ChatMessage(role="user", content=user_prompt))
    return GenerationRequest(
        messages=messages,
        model=model or DEFAULT_CHAT_MODEL,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )


def iter_stream_text(stream: Any) -> Iterator[str]:
    for event in stream:
        if getattr(event, "type", "") == "response.output_text.delta":
            delta = getattr(event, "delta", "")
            if delta:
                yield delta
