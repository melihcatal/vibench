import os
from anthropic import Anthropic


def archive_summary(transcript: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required.")
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this meeting transcript:\n\n{transcript}",
            },
        ],
    )
    return message.content[0].text
