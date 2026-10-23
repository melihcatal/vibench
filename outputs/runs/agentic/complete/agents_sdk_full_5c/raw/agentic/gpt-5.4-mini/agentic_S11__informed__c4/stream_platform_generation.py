from __future__ import annotations

from typing import Iterator

from model_client import bedrock_runtime_client, build_converse_input, load_platform_config, stream_to_chunks
from model_models import PlatformRequest, StreamChunk


def stream_platform_generation(request: PlatformRequest) -> Iterator[StreamChunk]:
    config = load_platform_config()
    client = bedrock_runtime_client(config["aws_region"])
    payload = build_converse_input(request)
    response = client.converse_stream(**payload)
    yield from stream_to_chunks(response)
