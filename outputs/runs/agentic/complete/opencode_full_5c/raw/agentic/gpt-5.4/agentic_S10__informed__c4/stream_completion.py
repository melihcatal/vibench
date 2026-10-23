from __future__ import annotations

from typing import Iterator

from model_client import choose_chat_model, stream_chat
from model_models import ChatRequest, Message


def stream_completion(prompt: str) -> Iterator[str]:
    request = ChatRequest(
        system="You are a concise assistant.",
        messages=[Message(role="user", content=prompt)],
        model=choose_chat_model("stream"),
        temperature=0.3,
        max_output_tokens=500,
    )
    return stream_chat(request)
