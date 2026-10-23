import os
from anthropic import Anthropic
from typing import Dict, Any


def onboarding_summary(onboarding_data: Dict[str, Any], locale: str = "en") -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    client = Anthropic(api_key=api_key)
    prompt = f"Summarize the onboarding state for support purposes in {locale}:\n{onboarding_data}"
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
