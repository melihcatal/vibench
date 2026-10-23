from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from model_models import ChatMessage, GenerationConfig


DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_MODERATION_MODEL = os.getenv(
    "OPENAI_MODERATION_MODEL", "omni-moderation-latest"
)


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def resolve_chat_config(
    model: str | None = None, temperature: float = 0.2, max_output_tokens: int = 512
) -> GenerationConfig:
    return GenerationConfig(
        model=model or DEFAULT_CHAT_MODEL,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )


def messages_to_dicts(messages: Iterable[ChatMessage]) -> List[dict]:
    return [message.to_dict() for message in messages]
