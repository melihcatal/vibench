import os
from anthropic import Anthropic


def onboarding_summary(onboarding_state: str) -> dict:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarize this onboarding state for support:\n{onboarding_state}"}],
    )
    text = "".join(part.text for part in message.content if hasattr(part, "text"))
    return {"summary": text}
