import os
from anthropic import Anthropic
from typing import Dict, Any

def onboarding_summary(onboarding_state: Dict[str, Any]) -> str:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY not set')
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=500,
        messages=[
            {
                'role': 'user',
                'content': f'Provide a concise summary of this user onboarding state for support team: {onboarding_state}'
            }
        ]
    )
    return message.content[0].text