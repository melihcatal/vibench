from typing import Iterator
from cohere.types import StreamedChatResponse

from model_client import get_cohere_client

def stream_generation(prompt: str) -> Iterator[StreamedChatResponse]:
    """
    Streams output from a Cohere model.

    Args:
        prompt: The input text prompt.

    Yields:
        Provider-specific response objects from the Cohere stream.
    """
    client = get_cohere_client()
    
    stream = client.chat_stream(
        model="command-r-plus",
        message=prompt
    )
    
    for event in stream:
        yield event
