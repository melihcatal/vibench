import os

from anthropic import Anthropic


def onboarding_summary(state_text: str):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this onboarding state for support: {state_text}",
            }
        ],
    )
    return message.content[0].text if message.content else ""
