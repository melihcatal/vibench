from __future__ import annotations

from typing import Iterator

from model_client import get_openai_client
from model_models import PlatformRequest, build_messages
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: PlatformRequest) -> Iterator[object]:
    client = get_openai_client()
    model = select_platform_resource(task="chat", override_model=request.model_hint)
    with client.responses.stream(
        model=model,
        input=build_messages(request),
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    ) as stream:
        for event in stream:
            yield event
