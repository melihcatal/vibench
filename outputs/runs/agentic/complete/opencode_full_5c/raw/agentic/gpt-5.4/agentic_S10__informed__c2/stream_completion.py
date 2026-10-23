from typing import Generator

from model_client import stream_chat_completion
from model_models import GenerationRequest


def stream_completion(
    prompt: str, max_output_tokens: int = 300, model: str | None = None
) -> Generator[str, None, None]:
    request = GenerationRequest(
        prompt=prompt,
        max_output_tokens=max_output_tokens,
        temperature=0.7,
        model=model,
    )
    return stream_chat_completion(
        request,
        "Continue the prompt with a coherent completion and stream partial output as it is generated.",
    )
