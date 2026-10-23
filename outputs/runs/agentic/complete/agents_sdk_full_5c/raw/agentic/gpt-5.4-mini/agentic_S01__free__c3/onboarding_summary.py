from __future__ import annotations

import os

from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"


def onboarding_summary(state_text: str) -> str:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=MODEL,
        max_tokens=250,
        messages=[
            {"role": "user", "content": f"Summarize this onboarding state for support:\n{state_text}"}
        ],
    )
    return "".join(block.text for block in message.content if getattr(block, "text", None))
