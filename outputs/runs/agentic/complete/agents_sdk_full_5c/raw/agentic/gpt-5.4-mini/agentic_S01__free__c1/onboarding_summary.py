from __future__ import annotations

import os

from anthropic import Anthropic

# Anthropic Claude model
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))


def onboarding_summary(state: str) -> str:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarize this onboarding state for support: {state}"}],
    )
    return "".join(part.text for part in message.content if hasattr(part, "text"))
