from typing import Any, Dict, Iterator, Optional

from openai import OpenAI

from model_client import get_openai_client, get_model_name, resolve_generation_input
from model_models import ModelRequest, StreamChunk, normalize_stream_chunk


def stream_platform_generation(request: Dict[str, Any] | ModelRequest, client: Optional[OpenAI] = None) -> Iterator[StreamChunk]:
    normalized = resolve_generation_input(request)
    api_client = client or get_openai_client()
    model = get_model_name(normalized.model)
    stream = api_client.responses.create(
        model=model,
        input=normalized.prompt,
        temperature=normalized.temperature,
        max_output_tokens=normalized.max_output_tokens,
        stream=True,
    )
    for event in stream:
        yield normalize_stream_chunk(event, provider="openai", model=model)
