"""
Summarize long text using the Mistral AI hosted LLM.

Provider: Mistral AI Chat API
SDK: mistralai
Auth: MISTRAL_API_KEY
"""

from __future__ import annotations

from typing import Optional

from model_client import build_request, create_mistral_client, execute_chat
from model_models import (
    LLMResponse,
    LLMRequest,
    build_summarization_prompt,
)


def summarize_text(
    text: str,
    max_length: int = 200,
    model: Optional[str] = None,
    temperature: float = 0.5,
) -> LLMResponse:
    """Summarize the given text using a Mistral AI model.

    Args:
        text: The long text to summarize.
        max_length: Approximate maximum word count for the summary.
        model: Optional concrete Mistral model identifier (e.g., 'mistral-large-latest').
        temperature: Sampling temperature.

    Returns:
        LLMResponse with the summarized content.
    """
    prompt = build_summarization_prompt(text, max_length=max_length)

    system_prompt = (
        "You are an expert summarizer. Produce clear, concise summaries that capture "
        "the essential points of the provided text."
    )

    request = build_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=2048,
        temperature=temperature,
    )

    return execute_chat(request)


def summarize_text_with_client(
    text: str,
    client,
    max_length: int = 200,
    model: Optional[str] = None,
    temperature: float = 0.5,
) -> LLMResponse:
    """Summarize text using a pre-created Mistral client.

    Args:
        text: The long text to summarize.
        client: An initialized mistralai.Mistral client.
        max_length: Approximate maximum word count for the summary.
        model: Optional concrete Mistral model identifier.
        temperature: Sampling temperature.

    Returns:
        LLMResponse with the summarized content.
    """
    prompt = build_summarization_prompt(text, max_length=max_length)

    system_prompt = (
        "You are an expert summarizer. Produce clear, concise summaries that capture "
        "the essential points of the provided text."
    )

    request = build_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=2048,
        temperature=temperature,
    )

    return execute_chat(request, client=client)
