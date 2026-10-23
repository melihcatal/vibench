from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from model_client import get_azure_openai_client, get_chat_deployment
from model_models import PlatformRequest


def stream_platform_generation(request: PlatformRequest) -> Iterator[Any]:
    client = get_azure_openai_client()
    stream = client.chat.completions.create(
        model=get_chat_deployment(),
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    for event in stream:
        yield event
