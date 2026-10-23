from anthropic import Anthropic
import os
from typing import Dict, Any

def summarize_onboarding_state(onboarding_data: Dict[str, Any]) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    model = "claude-3-sonnet-20240229"

    prompt = f"Summarize the following onboarding state for support:
    {onboarding_data}"

    response = client.messages.create(
        model=model,
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def onboarding_summary(onboarding_data: Dict[str, Any]) -> str:
    return summarize_onboarding_state(onboarding_data)

if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) == 2:
        onboarding_data = json.loads(sys.argv[1])
        summary = onboarding_summary(onboarding_data)
        print(f"Summary: {summary}")