from typing import Iterator

from model_client import get_client
from model_models import PlatformRequest, build_messages
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: PlatformRequest) -> Iterator[object]:
    resource = select_platform_resource("chat", request.resource_id)
    client = get_client()
    stream = client.responses.create(
        model=resource["resource_id"],
        input=build_messages(request),
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
        stream=True,
    )
    for event in stream:
        yield event
