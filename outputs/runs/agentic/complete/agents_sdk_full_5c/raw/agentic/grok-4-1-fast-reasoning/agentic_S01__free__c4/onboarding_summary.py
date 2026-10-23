import os
import json
from anthropic import Anthropic
from typing import Dict, Any

def generate_onboarding_summary(onboarding_state: Dict[str, Any]) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    client = Anthropic(api_key=api_key)
    state_json = json.dumps(onboarding_state, indent=2)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[{"role": "user", "content": f"Summarize this onboarding state for support: {state_json}"}]
    )
    return message.content[0].text