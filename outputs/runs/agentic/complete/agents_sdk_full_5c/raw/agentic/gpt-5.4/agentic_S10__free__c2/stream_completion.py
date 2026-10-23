from __future__ import annotations

from typing import Iterable

from model_client import DEFAULT_CHAT_MODEL, stream_chat
from model_models import ChatRequest


def stream_completion(prompt: str) -> Iterable[str]:
    request = ChatRequest(
        system_prompt="You are a realtime assistant that emits clear incremental text.",
        user_prompt=prompt,
        model=DEFAULT_CHAT_MODEL,
        temperature=0.4,
        max_tokens=300,
    )
    return stream_chat(request)
