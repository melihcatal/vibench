from typing import Generator, Optional

from model_client import get_client, resolve_model_name
from model_models import PlatformStreamChunk, normalize_text


def stream_platform_generation(prompt: str, model: Optional[str] = None, temperature: float = 0.2):
    client = get_client()
    model_name = resolve_model_name(model)
    stream = client.responses.create(
        model=model_name,
        input=normalize_text(prompt),
        temperature=temperature,
        stream=True,
    )
    for event in stream:
        yield PlatformStreamChunk(event=event, model=model_name)
