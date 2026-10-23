from typing import Iterator
from model_client import get_model
from model_models import InvokeRequest, StreamChunk


def stream_generation(request: InvokeRequest) -> Iterator[StreamChunk]:
    model = get_model()
    stream = model.generate_content(request.prompt, stream=True)

    for chunk in stream:
        yield StreamChunk(text=chunk.text, raw_chunk=chunk)
