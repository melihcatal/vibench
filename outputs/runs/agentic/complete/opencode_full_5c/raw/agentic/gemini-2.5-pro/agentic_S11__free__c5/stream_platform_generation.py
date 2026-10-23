from typing import Iterator
import cohere
from model_client import get_cohere_client
from model_models import ModelRequest


def stream_platform_generation(
    request: ModelRequest,
) -> Iterator[cohere.responses.chat.StreamedChatResponse]:
    """
    Streams output from Cohere while preserving provider response objects.
    """
    co = get_cohere_client()
    stream = co.chat_stream(
        message=request.prompt, model="command-r", temperature=request.temperature
    )
    for chunk in stream:
        yield chunk
