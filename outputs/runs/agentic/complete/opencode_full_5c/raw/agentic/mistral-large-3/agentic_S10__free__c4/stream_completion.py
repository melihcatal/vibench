from typing import Optional, Iterator, Dict, Any
import os
from model_client import get_llm_client
from model_models import CompletionRequest, CompletionResponse


def stream_completion(
    prompt: str,
    max_tokens: int = 100,
    temperature: float = 0.7,
    model: Optional[str] = "mistral/mistral-large-latest",
) -> Iterator[str]:
    """
    Streams partial output tokens from a hosted LLM.

    Args:
        prompt: The input prompt to generate completions for.
        max_tokens: Maximum number of tokens to generate.
        temperature: Controls randomness in the generation.
        model: The model identifier for the hosted LLM.

    Returns:
        An iterator yielding partial tokens as they are generated.
    """
    client = get_llm_client()

    request = CompletionRequest(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model,
        stream=True,
    )

    for token in client.stream_completion(request):
        yield token
