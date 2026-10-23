from anthropic import Anthropic, MessageParam
import os
from typing import Dict, Any

def onboarding_summary(onboarding_state: Dict[str, Any]) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    state_str = str(onboarding_state)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarize this onboarding state for support team: {state_str}"}]
    )
    return message.content[0].text
