import os
from typing import Generator
import cohere
from cohere.types import StreamedChatResponse

from model_models import PlatformRequest

def stream_model_generation(request: PlatformRequest) -> Generator[StreamedChatResponse, None, None]:
    """
    Streams output from a Cohere model.

    Yields:
        Provider-specific response objects from the stream.
    """
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))
    
    stream = client.chat(
        model=request.model_id,
        message=request.prompt,
        max_tokens=request.max_tokens,
        stream=True
    )
    
    for event in stream:
        yield event
