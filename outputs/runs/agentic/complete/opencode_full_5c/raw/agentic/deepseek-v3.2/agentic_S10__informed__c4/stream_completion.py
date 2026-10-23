import os
from anthropic import Anthropic


def stream_completion(prompt: str, max_tokens: int = 1000):
    """
    Stream partial output tokens from Anthropic Claude.
    Yields chunks of text as they become available.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text
