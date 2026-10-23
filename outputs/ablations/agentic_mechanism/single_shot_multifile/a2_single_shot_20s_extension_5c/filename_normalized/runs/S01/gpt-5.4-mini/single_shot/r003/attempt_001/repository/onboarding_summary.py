from typing import Any, Dict

from anthropic import Anthropic


def onboarding_summary(state: Dict[str, Any]) -> str:
    client = Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Summarize this onboarding state for support: {state}"}],
    )
    return "".join(part.text for part in message.content if hasattr(part, "text"))
