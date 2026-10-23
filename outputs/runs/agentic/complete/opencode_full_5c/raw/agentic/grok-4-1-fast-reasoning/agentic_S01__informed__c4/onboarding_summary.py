import os
import anthropic
from typing import Dict, Any


def onboarding_summary(onboarding_data: Dict[str, Any]) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this user onboarding state for support review:\\n{onboarding_data}",
            }
        ],
    )
    return message.content[0].text
