import os
from anthropic import Anthropic


def summarize_transcript(
    transcript: str, model: str = "claude-3-5-sonnet-20240620", max_tokens: int = 1024
) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following transcript concisely:\n\n{transcript}",
            }
        ],
    )
    return message.content[0].text
