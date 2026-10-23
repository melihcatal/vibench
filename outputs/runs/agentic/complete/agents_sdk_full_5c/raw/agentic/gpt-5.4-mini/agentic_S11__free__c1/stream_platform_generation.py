from __future__ import annotations

from typing import Generator, Optional

from openai import OpenAI

from model_client import get_client
from model_models import NormalizedChunk, normalize_text
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str, resource_id: Optional[str] = None, client: Optional[OpenAI] = None) -> Generator[NormalizedChunk, None, None]:
    client = client or get_client()
    model = select_platform_resource(resource_id, client=client)
    stream = client.responses.create(model=model, input=prompt, stream=True)
    for event in stream:
        text = normalize_text(getattr(event, "delta", None) or getattr(event, "output_text", None) or getattr(event, "text", None))
        yield NormalizedChunk(text=text, raw=event)
