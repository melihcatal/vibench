from __future__ import annotations

from collections.abc import Iterator

from model_client import build_generative_model, load_platform_selection
from model_models import GenerationRequest, StreamChunk



def stream_platform_generation(request: GenerationRequest) -> Iterator[StreamChunk]:
    selection = load_platform_selection()
    model = build_generative_model(selection)
    stream = model.generate_content(
        request.to_messages(),
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
        stream=True,
    )
    for provider_response in stream:
        yield StreamChunk(
            text=getattr(provider_response, "text", ""),
            raw=provider_response,
        )
