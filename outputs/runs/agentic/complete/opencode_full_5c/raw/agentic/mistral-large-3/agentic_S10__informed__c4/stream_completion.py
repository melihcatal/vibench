from typing import Dict, Any, Iterator

from model_client import get_llm_client
from model_models import LLMRequest, LLMResponseChunk


def stream_completion(
    prompt: str,
    model_family: str = "mistral",
    model_identifier: str = "mistral-large-latest",
    max_tokens: int = 1000,
    temperature: float = 0.7,
    **kwargs: Dict[str, Any],
) -> Iterator[str]:
    """
    Streams partial output tokens from a hosted LLM.

    Args:
        prompt: Input prompt for the LLM.
        model_family: The model family to use (e.g., "mistral").
        model_identifier: The specific model identifier (e.g., "mistral-large-latest").
        max_tokens: Maximum number of tokens in the response.
        temperature: Sampling temperature.
        **kwargs: Additional model-specific parameters.

    Yields:
        Partial output tokens as they are generated.
    """
    client = get_llm_client(model_family)

    request = LLMRequest(
        model_identifier=model_identifier,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
        **kwargs,
    )

    for chunk in client.stream(request):
        yield chunk.text
