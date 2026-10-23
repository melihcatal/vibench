import os
from typing import Dict

from anthropic import Anthropic


MODEL = "claude-3-5-sonnet-20241022"


def onboarding_summary(state: str) -> Dict[str, str]:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": f"Summarize this onboarding state for support: {state}"}],
    )
    return {"summary": message.content[0].text}
