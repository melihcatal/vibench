from __future__ import annotations

from typing import Iterator

from model_client import HostedModelClient
from model_models import GenerationOptions, build_messages


def stream_completion(prompt: str) -> Iterator[str]:
    client = HostedModelClient()
    model = client.select_model_family("stream")
    messages = build_messages(
        system_prompt="You are a responsive assistant that streams a helpful completion.",
        user_prompt=prompt,
    )
    return client.stream_chat(
        messages,
        GenerationOptions(model=model, temperature=0.4, max_tokens=300),
    )
