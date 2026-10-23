import os
from anthropic import Anthropic


def summarize_onboarding_state(onboarding_data: str) -> str:
    """Summarizes onboarding state for support using Anthropic's Messages API (Claude 3 Haiku)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",  # Using Claude 3 Haiku as a concrete model identifier
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize the following onboarding state for a support agent: {onboarding_data}",
                }
            ],
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error summarizing with Anthropic: {e}")
        raise
