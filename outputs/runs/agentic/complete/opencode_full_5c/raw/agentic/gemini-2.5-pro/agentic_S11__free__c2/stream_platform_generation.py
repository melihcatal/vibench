import os
import cohere
from typing import Iterator
from model_models import PlatformRequest


def stream_model_generation(
    request: PlatformRequest,
) -> Iterator[cohere.StreamedChatResponse]:
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))

    stream = client.chat_stream(
        model=request.model_id,
        message=request.prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    for event in stream:
        yield event
