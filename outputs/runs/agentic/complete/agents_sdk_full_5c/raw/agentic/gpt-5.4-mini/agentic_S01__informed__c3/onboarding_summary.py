from __future__ import annotations

from typing import Any, Dict

from anthropic import Anthropic

CLAUDE_MODEL = "claude-3-5-sonnet-20240620"


def onboarding_summary(state_text: str) -> Dict[str, Any]:
    client = Anthropic()
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarize this onboarding state for support:\n{state_text}"}],
    )
    return {"provider": "Anthropic Messages API", "model": CLAUDE_MODEL, "summary": message.content[0].text}
