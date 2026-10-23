from __future__ import annotations

import json
import os
from typing import Iterable, List, Optional

from openai import OpenAI

from model_models import ChatMessage, GenerationConfig, normalize_messages


DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def build_messages(system_prompt: Optional[str], user_prompt: str) -> List[ChatMessage]:
    messages: List[ChatMessage] = []
    if system_prompt:
        messages.append(ChatMessage(role="system", content=system_prompt))
    messages.append(ChatMessage(role="user", content=user_prompt))
    return messages


def chat_completion_text(
    messages: List[ChatMessage],
    model: str = DEFAULT_CHAT_MODEL,
    config: Optional[GenerationConfig] = None,
) -> str:
    client = get_openai_client()
    cfg = config or GenerationConfig()
    response = client.chat.completions.create(
        model=model,
        messages=normalize_messages(messages),
        temperature=cfg.temperature,
        max_completion_tokens=cfg.max_output_tokens,
        top_p=cfg.top_p,
    )
    return response.choices[0].message.content or ""


def chat_completion_json(
    messages: List[ChatMessage],
    model: str = DEFAULT_CHAT_MODEL,
    config: Optional[GenerationConfig] = None,
) -> dict:
    client = get_openai_client()
    cfg = config or GenerationConfig()
    response = client.chat.completions.create(
        model=model,
        messages=normalize_messages(messages),
        response_format={"type": "json_object"},
        temperature=cfg.temperature,
        max_completion_tokens=cfg.max_output_tokens,
        top_p=cfg.top_p,
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)


def stream_chat_completion(
    messages: List[ChatMessage],
    model: str = DEFAULT_CHAT_MODEL,
    config: Optional[GenerationConfig] = None,
) -> Iterable[str]:
    client = get_openai_client()
    cfg = config or GenerationConfig()
    stream = client.chat.completions.create(
        model=model,
        messages=normalize_messages(messages),
        temperature=cfg.temperature,
        max_completion_tokens=cfg.max_output_tokens,
        top_p=cfg.top_p,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
