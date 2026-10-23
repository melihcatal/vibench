import anthropic
import os

def summarize_secret_rotation_status(rotation_status_text: str) -> str:
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    message = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=1024,
        temperature=0.7,
        messages=[
            {
                'role': 'user',
                'content': f'Provide a concise summary of the secret rotation status:\\n\\n{rotation_status_text}'
            }
        ]
    )
    return message.content[0].text
