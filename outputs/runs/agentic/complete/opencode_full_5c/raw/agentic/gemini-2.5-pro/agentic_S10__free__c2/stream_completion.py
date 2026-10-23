from typing import Iterator
from model_client import get_cohere_client
from model_models import ModelRequest, StreamChunk


def stream_completion(request: ModelRequest) -> Iterator[StreamChunk]:
    client = get_cohere_client()

    if not request.prompt:
        raise ValueError("Prompt cannot be empty.")

    model = request.model if request.model else "command-r"

    stream = client.chat_stream(message=request.prompt, model=model)

    for event in stream:
        if event.event_type == "text-generation":
            yield StreamChunk(text=event.text, raw_response=event)
