from __future__ import annotations

from typing import Iterator

from model_client import build_generation_config, stream_chat_completion
from model_models import ChatMessage, StreamChunk


def stream_completion(prompt: str) -> Iterator[StreamChunk]:
    messages = [
        ChatMessage(role="system", content="You are a real-time assistant. Stream a direct answer as tokens become available."),
        ChatMessage(role="user", content=prompt),
    ]
    for text in stream_chat_completion(
        messages,
        config=build_generation_config(model="gpt-4o-mini", temperature=0.5, max_tokens=300),
    ):
        yield StreamChunk(text=text, done=False)
    yield StreamChunk(text="", done=True)
