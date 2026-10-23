import os
from anthropic import Anthropic


def summarize_onboarding_state(onboarding_data: str) -> str:
    """
    Summarizes the onboarding state for a user using Anthropic's Claude.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following user onboarding state for a support ticket:\n\n{onboarding_data}",
                }
            ],
        )
        return message.content[0].text
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error summarizing onboarding state: {e}"
