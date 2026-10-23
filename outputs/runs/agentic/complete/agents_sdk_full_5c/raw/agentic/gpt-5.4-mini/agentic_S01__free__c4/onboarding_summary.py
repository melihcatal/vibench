from __future__ import annotations

import os

from anthropic import Anthropic


MODEL_ID = "claude-3-5-sonnet-20240620"


def onboarding_summary(state: str) -> str:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=MODEL_ID,
        max_tokens=300,
        messages=[
            {"role": "user", "content": f"Summarize this onboarding state for support:\n\n{state}"}
        ],
    )
    return "".join(part.text for part in message.content if hasattr(part, "text"))
