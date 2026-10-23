from typing import Iterator
from model_client import get_cohere_client
from model_models import ModelRequest, StreamedModelResponse


def stream_model_generation(request: ModelRequest) -> Iterator[StreamedModelResponse]:
    cohere_client = get_cohere_client()

    stream = cohere_client.chat(
        model=request.model, message=request.prompt, stream=True
    )

    for event in stream:
        if event.event_type == "text-generation":
            yield StreamedModelResponse(text_chunk=event.text, provider_object=event)
