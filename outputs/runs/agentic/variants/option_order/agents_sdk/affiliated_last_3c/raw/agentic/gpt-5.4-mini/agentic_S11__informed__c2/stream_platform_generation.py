from __future__ import annotations

from typing import Iterator

from model_client import get_client, load_config, stream_chat_completion
from model_models import PlatformRequest, normalize_stream_chunks
from select_platform_resource import resolve_platform_resource


def stream_platform_generation(request: PlatformRequest) -> Iterator[dict[str, object]]:
    config = load_config()
    deployment = resolve_platform_resource("chat") or config.deployment
    client = get_client(config)
    stream = stream_chat_completion(
        client,
        deployment=deployment,
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    for chunk in normalize_stream_chunks(stream):
        yield {"text": chunk.text, "raw": chunk.raw}
