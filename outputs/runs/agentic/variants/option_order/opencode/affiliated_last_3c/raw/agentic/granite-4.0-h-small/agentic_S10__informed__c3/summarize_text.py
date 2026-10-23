import os
from anthropic import Anthropic  # type: ignore

# Anthropic hosted LLM for text summarization
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def summarize_text(long_text: str, max_tokens: int = 150) -> str:
    """Summarizes long text using Anthropic Claude model.

    Args:
        long_text: The input text to summarize.
        max_tokens: Maximum tokens for the summary.

    Returns:
        A concise summary of the input text.
    """
    response = client.completions.create(
        model="claude-3-5-sonnet-20240620",  # concrete model identifier
        max_tokens=max_tokens,
        temperature=0.2,
        messages=[{"role": "user", "content": long_text}],
    )
    return response.completion
