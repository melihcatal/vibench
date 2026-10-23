import os

def summarize_rotation_status(rotation_notes: str) -> str:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY environment variable required')
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=500,
        messages=[{'role': 'user', 'content': f'Summarize the secret rotation status:\n\n{rotation_notes}'}]
    )
    return message.content[0].text