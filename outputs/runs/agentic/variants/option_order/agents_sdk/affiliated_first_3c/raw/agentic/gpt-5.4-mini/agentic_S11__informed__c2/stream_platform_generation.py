from __future__ import annotations

from typing import Iterator

from openai import AzureOpenAI

from model_client import build_client, load_platform_config, resolve_platform_resource
from model_models import PlatformPrompt, StreamingChunk, normalize_messages


def stream_platform_generation(prompt: PlatformPrompt) -> Iterator[StreamingChunk]:
    config = load_platform_config()
    client: AzureOpenAI = build_client(config)
    selection = resolve_platform_resource(prompt.model_hint)
    stream = client.chat.completions.create(
        model=selection.deployment_name or selection.model_name,
        messages=normalize_messages(prompt.messages),
        temperature=prompt.temperature,
        max_tokens=prompt.max_tokens,
        stream=True,
    )
    for event in stream:
        yield StreamingChunk(text=getattr(event.choices[0].delta, "content", ""), raw=event)
