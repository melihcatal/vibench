import os
from anthropic import Anthropic

def archive_summary(transcript: str, max_tokens: int = 1000) -> str:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY environment variable is required.')
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=max_tokens,
        messages=[{'role': 'user', 'content': f'Summarize this transcript concisely:\n\n{transcript}'}]
    )
    return message.content[0].text