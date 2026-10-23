from __future__ import annotations

from typing import Generator

from model_client import stream_chat_completion
from model_models import ChatRequest


def stream_completion(
    prompt: str, model: str | None = None
) -> Generator[str, None, None]:
    request = ChatRequest(
        system_prompt="You are an OpenAI streaming completion assistant.",
        user_prompt=prompt,
        model=model,
        temperature=0.3,
        max_tokens=400,
    )
    yield from stream_chat_completion(request)
