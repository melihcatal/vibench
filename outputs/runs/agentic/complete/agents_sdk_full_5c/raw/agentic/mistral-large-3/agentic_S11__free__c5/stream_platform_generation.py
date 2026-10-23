import os
from typing import Iterator
from model_client import get_model_client
from model_models import ModelRequest

def stream_model_generation(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    model_identifier: str = "command-r-plus",
) -> Iterator[str]:
    """
    Streams output from the Cohere Command R+ model while preserving provider response objects.
    Yields text chunks as they are generated.
    """
    client = get_model_client()
    request = ModelRequest(
        message=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        model=model_identifier,
    )

    for response in client.chat_stream(
        model=request.model,
        message=request.message,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    ):
        if response.event_type == "text-generation":
            yield response.text