from __future__ import annotations

from typing import Iterator

from model_client import OpenAIModelClient, build_text_request


def stream_completion(prompt: str, *, model: str = "gpt-4o-mini") -> Iterator[str]:
    client = OpenAIModelClient(model=model)
    request = build_text_request(
        system_prompt="You are a helpful assistant that responds clearly and incrementally.",
        user_prompt=prompt,
        model=model,
        temperature=0.4,
        max_tokens=400,
        stream=True,
    )
    yield from client.stream(request)
