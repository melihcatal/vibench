from typing import Iterator
from model_client import client
from model_models import StreamedChatResponse

def get_streamed_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from the Cohere chat API.
    """
    stream = client.chat_stream(
        message=prompt,
        model="command-r"
    )
    
    response_iterator = StreamedChatResponse(stream)
    yield from response_iterator
