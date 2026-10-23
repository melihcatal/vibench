import os
from typing import Optional
from model_client import get_llm_client
from model_models import SummarizationRequest, SummarizationResponse


def summarize_text(
    text: str,
    model_family: str = "gemini",
    model_id: str = "gemini-1.5-flash-001",
    temperature: float = 0.7,
    max_tokens: int = 150,
    **kwargs
) -> Optional[str]:
    """
    Summarize long text using a hosted LLM.
    
    Args:
        text: Input text to summarize.
        model_family: The model family to use (e.g., 'gemini').
        model_id: The specific model identifier (e.g., 'gemini-1.5-flash-001').
        temperature: Sampling temperature.
        max_tokens: Maximum number of tokens to generate.
        **kwargs: Additional model-specific parameters.
        
    Returns:
        Generated summary or None if failed.
    """
    client = get_llm_client(model_family)
    if not client:
        return None

    request = SummarizationRequest(
        text=text,
        model_id=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    response = client.summarize(request)
    return response.summary if isinstance(response, SummarizationResponse) else None