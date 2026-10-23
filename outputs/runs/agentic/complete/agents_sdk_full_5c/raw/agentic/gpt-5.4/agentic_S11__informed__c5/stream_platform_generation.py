from __future__ import annotations

from typing import Generator, Iterable

from model_client import get_azure_openai_client
from model_models import GenerationRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: GenerationRequest) -> Iterable[object]:
    resource = select_platform_resource(task="chat")
    client = get_azure_openai_client()
    stream = client.chat.completions.create(
        model=resource["deployment"],
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_output_tokens,
        stream=True,
    )
    for event in stream:
        yield event


def stream_text_chunks(request: GenerationRequest) -> Generator[str, None, None]:
    for event in stream_platform_generation(request):
        if getattr(event, "choices", None):
            delta = getattr(event.choices[0], "delta", None)
            content = getattr(delta, "content", None)
            if content:
                yield content
