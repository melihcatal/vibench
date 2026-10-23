from __future__ import annotations

from typing import Iterator

from model_client import get_azure_openai_client
from model_models import ChatRequest
from select_platform_resource import select_platform_resource



def stream_platform_generation(request: ChatRequest) -> Iterator[object]:
    client = get_azure_openai_client()
    deployment = select_platform_resource([request.resource_name] if request.resource_name else None)
    stream = client.responses.stream(
        model=deployment,
        input=request.to_messages(),
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
    )
    with stream as events:
        for event in events:
            yield event
