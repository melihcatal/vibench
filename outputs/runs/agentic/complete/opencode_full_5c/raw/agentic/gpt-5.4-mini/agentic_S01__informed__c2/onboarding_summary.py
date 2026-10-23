from anthropic import Anthropic


def onboarding_summary(state: str) -> str:
    client = Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this onboarding state for support: {state}",
            }
        ],
    )
    return message.content[0].text if message.content else ""
