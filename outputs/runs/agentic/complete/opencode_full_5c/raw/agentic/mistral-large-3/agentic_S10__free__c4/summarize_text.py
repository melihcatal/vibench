from typing import Optional, Dict, Any
import os
from model_client import get_llm_client
from model_models import SummarizationRequest, SummarizationResponse


def summarize_text(
    text: str,
    max_tokens: int = 150,
    temperature: float = 0.3,
    model: Optional[str] = "mistral/mistral-large-latest",
) -> str:
    """
    Summarizes long text using a hosted LLM.

    Args:
        text: The input text to summarize.
        max_tokens: Maximum number of tokens in the summary.
        temperature: Controls randomness in the summary.
        model: The model identifier for the hosted LLM.

    Returns:
        The summarized text.
    """
    client = get_llm_client()

    request = SummarizationRequest(
        input_text=text, max_tokens=max_tokens, temperature=temperature, model=model
    )

    response = client.summarize(request)
    return response.summary
