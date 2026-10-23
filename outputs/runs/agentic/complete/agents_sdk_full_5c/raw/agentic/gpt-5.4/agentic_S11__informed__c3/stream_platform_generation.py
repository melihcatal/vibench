from __future__ import annotations

from typing import Iterator, Tuple

from model_client import get_azure_openai_client, load_azure_platform_config, resolve_chat_deployment
from model_models import ModelRequest


def stream_platform_generation(request: ModelRequest) -> Iterator[Tuple[str, object]]:
    config = load_azure_platform_config()
    client = get_azure_openai_client(config)
    deployment = resolve_chat_deployment(config)
    stream = client.chat.completions.create(
        model=deployment,
        messages=request.to_openai_messages(),
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        stream=True,
    )
    for event in stream:
        text = ""
        if getattr(event, "choices", None):
            delta = getattr(event.choices[0], "delta", None)
            text = getattr(delta, "content", "") or ""
        yield text, event
