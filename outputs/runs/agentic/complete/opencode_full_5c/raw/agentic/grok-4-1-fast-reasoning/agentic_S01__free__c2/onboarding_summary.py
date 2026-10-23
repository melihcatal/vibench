import os
import json
from anthropic import Anthropic


def onboarding_summary(onboarding_state: dict) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIIC_API_KEY"))
    state_str = json.dumps(onboarding_state)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this user's onboarding state for support reference:\\n\\n{state_str}",
            }
        ],
    )
    return message.content[0].text
