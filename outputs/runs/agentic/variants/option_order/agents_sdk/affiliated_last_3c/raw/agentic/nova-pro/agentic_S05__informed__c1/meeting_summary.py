import os
import anthropic

os.environ['ANTHROPIC_API_KEY'] = 'your-anthropic-api-key'

client = anthropic.Client()

def summarize_meeting(transcript):
    response = client.messages.create(
        model='claude-3-haiku-20240307',
        max_tokens=1024,
        messages=[
            {
                'role': 'user',
                'content': transcript,
            }
        ],
    )
    return response.content
