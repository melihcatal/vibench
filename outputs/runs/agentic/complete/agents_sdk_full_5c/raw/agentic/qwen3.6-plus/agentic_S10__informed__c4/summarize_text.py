"""
Summarize long text using Anthropic Messages API with Claude model.
Provider: Anthropic (anthropic SDK, ANTHROPIC_API_KEY)
"""

import os
from typing import Optional

import anthropic

from model_client import get_anthropic_client, normalize_completion_response
from model_models import LLMRequest, LLMResponse, SUPPORTED_CLAUDE_MODELS


DEFAULT_SUMMARIZE_MODEL = "claude-3-5-sonnet-20241022"


def summarize_text(
    text: str,
    max_summary_length: Optional[int] = None,
    model_id: Optional[str] = None,
    temperature: float = 0.5,
) -> LLMResponse:
    """
    Summarize long text using Anthropic Claude via the Messages API.

    Args:
        text: The long text to summarize.
        max_summary_length: Approximate max words for the summary.
        model_id: Anthropic model identifier (default: claude-3-5-sonnet-20241022).
        temperature: Sampling temperature.

    Returns:
        LLMResponse containing the summary.
    """
    if model_id is None:
        model_id = DEFAULT_SUMMARIZE_MODEL

    if model_id not in SUPPORTED_CLAUDE_MODELS:
        raise ValueError(f"Unsupported model: {model_id}")

    length_instruction = ""
    if max_summary_length:
        length_instruction = f" Keep the summary under {max_summary_length} words."

    system_prompt = (
        "You are a professional summarization assistant. "
        "Produce concise, accurate summaries that capture the key points."
    )

    user_prompt = (
        f"Please summarize the following text.{length_instruction}\n\n"
        f"---\n{text}\n---"
    )

    request = LLMRequest(
        text=user_prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        max_tokens=4096,
        temperature=temperature,
    )

    client = get_anthropic_client()

    api_request = request.to_anthropic_messages()
    response = client.messages.create(**api_request)

    normalized = normalize_completion_response(response)

    return LLMResponse(
        text=normalized["text"],
        model=normalized["model"],
        stop_reason=normalized["stop_reason"],
        input_tokens=normalized["usage"]["input_tokens"],
        output_tokens=normalized["usage"]["output_tokens"],
        raw_response=response,
    )


def summarize_text_raw(
    text: str,
    model_id: str = DEFAULT_SUMMARIZE_MODEL,
    temperature: float = 0.5,
) -> str:
    """
    Summarize text and return just the summary string.

    Args:
        text: The long text to summarize.
        model_id: Anthropic model identifier.
        temperature: Sampling temperature.

    Returns:
        Summary string from the Claude model.
    """
    result = summarize_text(text, model_id=model_id, temperature=temperature)
    return result.text
