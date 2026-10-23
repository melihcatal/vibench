from typing import Iterator
from cohere.types import StreamedChatResponse
from model_client import get_cohere_client

def stream_generation(prompt: str) -> Iterator[StreamedChatResponse]:
    """
    Streams output from a managed model platform, preserving provider response objects.

    Args:
        prompt: The input prompt to the model.

    Yields:
        The raw stream event objects from the Cohere API.
    """
    client = get_cohere_client()

    # The stream object from the Cohere client yields provider-specific event types
    stream = client.chat_stream(
        model="command-r",
        message=prompt,
    )

    for event in stream:
        yield event
