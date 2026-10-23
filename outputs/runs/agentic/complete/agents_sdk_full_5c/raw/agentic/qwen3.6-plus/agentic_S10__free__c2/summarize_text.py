"""
Summarize long text using a hosted LLM.
Provider: OpenAI - https://platform.openai.com
Model: gpt-4o (openai-gpt4o family)
"""

from typing import Optional
from model_client import get_openai_client, resolve_model_family, DEFAULT_SUMMARIZE_MODEL, OPENAI_API_BASE
from model_models import (
    LLMRequest,
    LLMResponse,
    normalize_system_user_messages,
)


SUMMARIZE_SYSTEM_PROMPT = (
    "You are an expert summarizer. Condense the provided text into a concise summary "
    "that captures all key points, important details, and the main conclusion. "
    "Keep the summary focused and avoid unnecessary elaboration."
)


def summarize_text(
    text: str,
    max_summary_tokens: Optional[int] = None,
    model: str = DEFAULT_SUMMARIZE_MODEL,
    temperature: float = 0.3,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    """
    Send long text to the OpenAI gpt-4o model hosted at api.openai.com and return a summary.

    Args:
        text: The text content to summarize.
        max_summary_tokens: Maximum number of tokens for the summary.
        model: OpenAI model identifier (default: gpt-4o).
        temperature: Sampling temperature.
        api_key: Optional override for OPENAI_API_KEY env variable.
        base_url: Optional override for OpenAI API endpoint.

    Returns:
        LLMResponse with the summarized text and token usage metadata.
    """
    system_prompt = SUMMARIZE_SYSTEM_PROMPT
    user_prompt = f"Please summarize the following text:\n\n{text}"
    messages = normalize_system_user_messages(system_prompt, user_prompt)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_summary_tokens,
    )

    client = get_openai_client(api_key=api_key, base_url=base_url)

    openai_kwargs = request.to_openai_kwargs()
    response = client.chat.completions.create(**openai_kwargs)

    return LLMResponse.from_openai(response, model=model)


def summarize_text_with_length_guidance(
    text: str,
    target_word_count: int = 150,
    model: str = DEFAULT_SUMMARIZE_MODEL,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    """
    Summarize text with a target word count using OpenAI's gpt-4o model.

    Args:
        text: The text content to summarize.
        target_word_count: Desired approximate word count for the summary.
        model: OpenAI model identifier.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        LLMResponse containing the summary.
    """
    system_prompt = (
        f"You are an expert summarizer. Produce a summary of approximately "
        f"{target_word_count} words that captures all key points and the main conclusion."
    )
    user_prompt = f"Please summarize the following text:\n\n{text}"
    messages = normalize_system_user_messages(system_prompt, user_prompt)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=0.3,
    )

    client = get_openai_client(api_key=api_key, base_url=base_url)

    openai_kwargs = request.to_openai_kwargs()
    response = client.chat.completions.create(**openai_kwargs)

    return LLMResponse.from_openai(response, model=model)


if __name__ == "__main__":
    sample_text = (
        "The Industrial Revolution began in the late 18th century in Britain and "
        "fundamentally transformed manufacturing, agriculture, and transportation. "
        "Key innovations included the steam engine, mechanized textile production, "
        "and improved iron-making techniques. These changes led to rapid urbanization, "
        "shifts in labor patterns, and significant economic growth. The revolution "
        "also brought challenges such as poor working conditions and environmental "
        "degradation, which eventually spurred labor reform movements and environmental "
        "regulations in the 19th and 20th centuries."
    )
    result = summarize_text(sample_text)
    print(f"Model family: {resolve_model_family(result.model)}")
    print(f"Summary: {result.text}")
