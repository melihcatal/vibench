import os
from typing import Iterator, Optional
from model_client import get_llm_client
from model_models import CompletionRequest, CompletionChunk


def stream_completion(
    prompt: str,
    model_family: str = "gemini",
    model_id: str = "gemini-1.5-pro-001",
    temperature: float = 0.7,
    max_tokens: int = 150,
    **kwargs
) -> Optional[Iterator[str]]:
    """
    Stream partial output tokens from a hosted LLM.
    
    Args:
        prompt: Input prompt to complete.
        model_family: The model family to use (e.g., 'gemini').
        model_id: The specific model identifier (e.g., 'gemini-1.5-pro-001').
        temperature: Sampling temperature.
        max_tokens: Maximum number of tokens to generate.
        **kwargs: Additional model-specific parameters.
        
    Returns:
        Iterator of partial tokens or None if failed.
    """
    client = get_llm_client(model_family)
    if not client:
        return None

    request = CompletionRequest(
        prompt=prompt,
        model_id=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    chunks = client.stream(request)
    if chunks:
        return (chunk.text for chunk in chunks if isinstance(chunk, CompletionChunk))
    return None