import os
import anthropic
from typing import List, Dict

def moderation_summary(decisions: List[Dict]) -> str:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY environment variable is required.')
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=500,
        system='Summarize the moderation decisions provided in a concise, professional brief. Highlight key patterns, counts of flagged/blocked, and notable cases.',
        messages=[
            {
                'role': 'user',
                'content': f'Please summarize these moderation decisions: {decisions}',
            },
        ],
    )
    return message.content[0].text
