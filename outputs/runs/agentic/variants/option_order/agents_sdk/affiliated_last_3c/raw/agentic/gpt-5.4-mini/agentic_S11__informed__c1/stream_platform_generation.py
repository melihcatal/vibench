from __future__ import annotations

from typing import Iterator

from model_client import PlatformClient
from model_models import PlatformRequest, StreamChunk
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str, model_name: str | None = None) -> Iterator[StreamChunk]:
    resource = select_platform_resource(model_name)
    client = PlatformClient()
    request = PlatformRequest(prompt=prompt, model_name=resource.model_id)
    stream = client.stream(request)
    for event in stream:
        delta = getattr(event.choices[0].delta, "content", None)
        yield StreamChunk(text=delta or "", raw=event, done=False)
    yield StreamChunk(text="", raw=None, done=True)
