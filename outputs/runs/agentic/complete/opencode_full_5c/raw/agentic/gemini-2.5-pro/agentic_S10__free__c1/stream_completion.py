from typing import Iterator
from model_client import get_model_client
from model_models import StreamCompletionRequest


def stream_completion(request: StreamCompletionRequest) -> Iterator[str]:
    cohere_client = get_model_client()

    stream = cohere_client.chat_stream(
        model=request.model,
        message=request.prompt,
    )

    for event in stream:
        if event.event_type == "text-generation":
            yield event.text
