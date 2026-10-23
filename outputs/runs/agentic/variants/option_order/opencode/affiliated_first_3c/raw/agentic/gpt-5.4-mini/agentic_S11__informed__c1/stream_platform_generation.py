from __future__ import annotations

from typing import Iterator

from model_client import get_platform_client
from model_models import PlatformRequest, normalize_messages
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str) -> Iterator[object]:
    client = get_platform_client()
    deployment = select_platform_resource()
    req = PlatformRequest(prompt=prompt)
    stream = client.chat.completions.create(
        model=deployment, messages=normalize_messages(req), stream=True
    )
    for chunk in stream:
        yield chunk
