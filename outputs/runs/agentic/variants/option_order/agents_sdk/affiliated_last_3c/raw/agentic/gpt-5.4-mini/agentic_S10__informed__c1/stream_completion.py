from __future__ import annotations

from typing import Iterator

from model_client import stream_text
from model_models import ChatRequest


def stream_completion(prompt: str) -> Iterator[str]:
    request = ChatRequest(
        model_family="chat",
        system="You are a helpful assistant that streams concise responses.",
        user=prompt,
        temperature=0.5,
        max_tokens=500,
        stream=True,
    )
    yield from stream_text(request)
