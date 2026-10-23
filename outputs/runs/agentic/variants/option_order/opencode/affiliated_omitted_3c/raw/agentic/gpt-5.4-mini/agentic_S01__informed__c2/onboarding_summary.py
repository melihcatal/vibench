from __future__ import annotations

from anthropic import Anthropic


def onboarding_summary(state: str) -> str:
    client = Anthropic()
    msg = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this onboarding state for support: {state}",
            }
        ],
    )
    return "".join(part.text for part in msg.content if hasattr(part, "text"))
