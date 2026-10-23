"""
Summarize long text using OpenAI hosted LLM inference.
Provider: OpenAI Chat Completions API (model: gpt-4o)
SDK: openai
Auth: OPENAI_API_KEY
"""

from typing import Optional
from model_client import get_client, DEFAULT_MODEL
from model_models import (
    LLMRequest,
    LLMResponse,
    build_summary_request,
)


def summarize_text(
    text: str,
    max_length: int = 150,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.3,
) -> LLMResponse:
    """
    Summarize long text using the OpenAI hosted LLM.

    Args:
        text: The long text to summarize.
        max_length: Approximate maximum word count for the summary.
        model: OpenAI model identifier (e.g., "gpt-4o", "gpt-4o-mini").
        temperature: Sampling temperature (lower = more deterministic).

    Returns:
        LLMResponse containing the summary and metadata.
    """
    request = build_summary_request(text, max_length=max_length)
    request.model = model
    request.temperature = temperature

    messages = request.to_messages()
    client = get_client()

    completion = client.create_chat_completion(
        messages=messages,
        model=request.model,
        temperature=request.temperature,
        max_tokens=1024,
    )

    return LLMResponse.from_openai_completion(completion)


def summarize_text_simple(
    text: str,
    max_words: int = 100,
) -> str:
    """
    Simple function to get just the summary string.

    Args:
        text: The text to summarize.
        max_words: Target word count.

    Returns:
        Summary string.
    """
    response = summarize_text(text, max_length=max_words)
    return response.content


if __name__ == "__main__":
    import os
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY environment variable is required.")
    else:
        sample_text = (
            "The history of computing spans several centuries, beginning with early "
            "mechanical calculators in the 17th century. Charles Babbage designed the "
            "Analytical Engine in the 1830s, considered the first general-purpose computer. "
            "Ada Lovelace wrote what is now recognized as the first computer program for "
            "Babbage's machine. The 20th century saw the development of electronic computers, "
            "starting with vacuum tube machines like ENIAC in 1945. The invention of the "
            "transistor in 1947 revolutionized computing, leading to smaller, faster, and "
            "more reliable machines. The microprocessor, developed in the 1970s, enabled "
            "personal computers to become widely available. Today, cloud computing and "
            "artificial intelligence represent the latest transformative shifts in the field."
        )
        result = summarize_text_simple(sample_text, max_words=50)
        print(f"Summary:\n{result}")
