import os
from anthropic import Anthropic


def summarize_text(text: str, max_tokens: int = 500) -> str:
    """
    Summarize long text using Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": f"Please summarize the following text concisely:\n\n{text}",
            }
        ],
    )

    return response.content[0].text
