from __future__ import annotations

from typing import Iterator

from model_client import choose_model, stream_text
from model_models import ChatTurn


def stream_completion(prompt: str, model: str | None = None) -> Iterator[str]:
    messages = [
        ChatTurn(
            role="system",
            content="You are a helpful assistant that streams concise completions.",
        ),
        ChatTurn(role="user", content=prompt.strip()),
    ]
    yield from stream_text(
        messages,
        model=choose_model("stream", model),
        temperature=0.4,
        max_output_tokens=300,
    )
