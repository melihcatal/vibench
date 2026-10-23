from __future__ import annotations

from typing import Iterator

from model_client import stream_chat_completion
from model_models import ChatMessage, GenerationRequest


def stream_completion(prompt: str, model: str = "gpt-4o-mini") -> Iterator[str]:
    request = GenerationRequest(
        model=model,
        temperature=0.7,
        max_tokens=300,
        messages=[
            ChatMessage(role="system", content="You are a helpful assistant that streams fluent responses."),
            ChatMessage(role="user", content=prompt),
        ],
    )
    return stream_chat_completion(request)
