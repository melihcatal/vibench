"""
Summarize long text using a hosted LLM.

Provider: OpenAI Chat Completions API
SDK: openai
Auth: OPENAI_API_KEY
Concrete model: gpt-4o-mini
Endpoint: api.openai.com/v1/chat/completions
"""

from typing import Optional

from model_client import call_llm_sync
from model_models import (
    LLMRequest,
    LLMResponse,
    build_summarization_request,
)


def summarize_text(
    text: str,
    max_words: int = 150,
    model_name: Optional[str] = None,
) -> LLMResponse:
    """
    Summarize the provided text using the OpenAI gpt-4o-mini model.

    Args:
        text: The long text to summarize.
        max_words: Maximum number of words in the summary.
        model_name: Optional override for the model identifier
                    (default: gpt-4o-mini).

    Returns:
        LLMResponse containing the generated summary.
    """
    effective_model = model_name or "gpt-4o-mini"
    request = build_summarization_request(
        text=text,
        max_words=max_words,
        model_name=effective_model,
    )
    return call_llm_sync(request)


def summarize_text_custom_prompt(
    text: str,
    system_prompt: str,
    model_name: str = "gpt-4o",
    temperature: float = 0.3,
) -> LLMResponse:
    """
    Summarize text with a custom system prompt via OpenAI.

    Args:
        text: The text to summarize.
        system_prompt: Custom system prompt directing the summarization.
        model_name: OpenAI model identifier (e.g., gpt-4o, gpt-4o-mini).
        temperature: Sampling temperature for generation.

    Returns:
        LLMResponse containing the summary.
    """
    request = LLMRequest(
        user_prompt=text,
        system_prompt=system_prompt,
        model_name=model_name,
        temperature=temperature,
        max_tokens=2048,
    )
    return call_llm_sync(request)
