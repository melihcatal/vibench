import os
import anthropic
from typing import Optional

def archive_summary(transcript: str, max_tokens: int = 500) -> str:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY environment variable is required.')
    
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=max_tokens,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": f"Please provide a concise summary of the following transcript:\n\n{transcript}"
            }
        ]
    )
    
    return message.content[0].text