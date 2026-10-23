from __future__ import annotations

from typing import Iterator

from model_client import HostedModelClient


def stream_completion(prompt: str) -> Iterator[str]:
    client = HostedModelClient()
    request = client.build_request(
        task="summarization",
        system_prompt="You are a helpful assistant. Stream a clear completion for the user request.",
        user_prompt=prompt,
        temperature=0.4,
        max_tokens=300,
    )
    return client.stream_text(request)
