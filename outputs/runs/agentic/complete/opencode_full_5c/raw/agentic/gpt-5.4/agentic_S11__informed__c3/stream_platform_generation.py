from __future__ import annotations

from typing import Iterable

from model_client import get_azure_openai_client
from model_models import PlatformRequest, iter_stream_objects
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: PlatformRequest) -> Iterable[object]:
    resource = select_platform_resource()
    client = get_azure_openai_client()
    stream = client.responses.stream(
        model=resource["resource_name"],
        input=request.to_messages(),
        max_output_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )
    with stream as events:
        for event in iter_stream_objects(events):
            yield event
