import os
from typing import Optional, Dict, Any

from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse


def summarize_text(
    text: str,
    model_family: str = "mistral",
    model_identifier: str = "mistral-large-latest",
    max_tokens: int = 150,
    temperature: float = 0.3,
    **kwargs: Dict[str, Any],
) -> str:
    """
    Summarizes long text using a hosted LLM.

    Args:
        text: Input text to summarize.
        model_family: The model family to use (e.g., "mistral").
        model_identifier: The specific model identifier (e.g., "mistral-large-latest").
        max_tokens: Maximum number of tokens in the summary.
        temperature: Sampling temperature.
        **kwargs: Additional model-specific parameters.

    Returns:
        Summarized text.
    """
    client = get_llm_client(model_family)

    prompt = f"Summarize the following text in a concise manner, limiting the summary to {max_tokens} tokens:\n\n{text}"
    request = LLMRequest(
        model_identifier=model_identifier,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs,
    )

    response: LLMResponse = client.generate(request)
    return response.text
