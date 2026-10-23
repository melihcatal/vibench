from __future__ import annotations

from typing import Iterable

from model_client import build_client
from model_models import ChatTurn, GenerationConfig


def stream_completion(prompt: str, model: str = "gpt-4o-mini") -> Iterable[str]:
    client = build_client()
    config = GenerationConfig(model=model, temperature=0.4, max_output_tokens=600)
    return client.stream_chat_text(
        [
            ChatTurn(role="system", content="You are a helpful assistant that streams concise completions."),
            ChatTurn(role="user", content=prompt),
        ],
        config=config,
    )
