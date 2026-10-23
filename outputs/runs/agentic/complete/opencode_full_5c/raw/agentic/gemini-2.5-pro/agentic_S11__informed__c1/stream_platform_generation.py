from typing import Iterator
from model_client import get_vertex_client
from vertexai.generative_models import GenerativeModel
from model_models import PlatformModelRequest, PlatformModelStreamChunk


def stream_model_generation(
    request: PlatformModelRequest,
) -> Iterator[PlatformModelStreamChunk]:
    """
    Streams output from a specified model on Vertex AI.
    """
    get_vertex_client()

    model = GenerativeModel(request.model_id)

    stream = model.generate_content(request.prompt, stream=True)

    for chunk in stream:
        yield PlatformModelStreamChunk(text=chunk.text, raw_chunk=chunk)
