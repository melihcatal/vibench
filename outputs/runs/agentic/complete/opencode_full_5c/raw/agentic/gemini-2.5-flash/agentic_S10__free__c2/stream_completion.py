from typing import Iterator
from model_client import VertexAIModelClient
from model_models import StreamCompletionRequest, StreamCompletionChunk


def stream_completion(
    request: StreamCompletionRequest,
) -> Iterator[StreamCompletionChunk]:
    client = VertexAIModelClient()
    return client.stream_completion(request)
