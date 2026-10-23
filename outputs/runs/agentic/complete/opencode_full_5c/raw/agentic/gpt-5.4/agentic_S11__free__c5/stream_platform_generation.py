from __future__ import annotations

from typing import Iterator

from model_client import get_bedrock_runtime_client, resolve_runtime_model_identifier
from model_models import ModelRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: ModelRequest) -> Iterator[dict]:
    resource = select_platform_resource()
    runtime_client = get_bedrock_runtime_client(resource.region_name)
    response = runtime_client.converse_stream(
        modelId=resolve_runtime_model_identifier(resource),
        messages=[{"role": "user", "content": [{"text": request.prompt}]}],
        inferenceConfig={
            "maxTokens": request.max_tokens,
            "temperature": request.temperature,
        },
    )
    stream = response.get("stream")
    if stream is None:
        return
    for event in stream:
        yield event
