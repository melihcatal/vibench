"""
Same-scenario: Summarize long text using a hosted LLM.

Provider: OpenAI GPT via OpenAI API
SDK: openai
Auth: OPENAI_API_KEY
Model: gpt-4o
"""

from typing import Optional

from model_client import create_openai_client, build_messages, get_default_model
from model_models import CompletionRequest, CompletionResponse


def summarize_text(
    text: str,
    model: Optional[str] = None,
    max_summary_tokens: int = 512,
    temperature: float = 0.5,
    system_prompt: Optional[str] = None,
) -> CompletionResponse:
    """
    Summarize a long piece of text using the OpenAI GPT-4o model.

    Args:
        text: The long text to summarize.
        model: The OpenAI model identifier. Defaults to gpt-4o.
        max_summary_tokens: Maximum tokens for the summary.
        temperature: Sampling temperature.
        system_prompt: Optional override for the system prompt.

    Returns:
        CompletionResponse containing the summary.
    """
    client = create_openai_client()

    default_system = (
        "You are an expert summarizer. "
        "Condense the provided text into a clear, concise summary "
        "that preserves the key points and important details. "
        "Write in the same language as the original text."
    )

    system_prompt = system_prompt or default_system
    user_prompt = f"Please summarize the following text:\n\n{text}"

    messages = build_messages(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    request = CompletionRequest(
        prompt=text,
        system_prompt=system_prompt,
        model=model or get_default_model(),
        temperature=temperature,
        max_tokens=max_summary_tokens,
    )

    response = client.chat.completions.create(
        **request.to_openai_kwargs(messages)
    )

    return CompletionResponse.from_openai_response(response)
