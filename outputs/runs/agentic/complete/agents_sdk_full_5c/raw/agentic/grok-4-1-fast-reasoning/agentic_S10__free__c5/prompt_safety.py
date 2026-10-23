import os
from anthropic import Anthropic

def is_unsafe(content: str) -> bool:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required.")
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=50,
        temperature=0,
        system="Evaluate if the content contains unsafe material like hate speech, violence, explicit sexual content, or harm. Respond ONLY with 'unsafe' or 'safe'.",
        messages=[{"role": "user", "content": content}]
    )
    return 'unsafe' in response.content.lower()