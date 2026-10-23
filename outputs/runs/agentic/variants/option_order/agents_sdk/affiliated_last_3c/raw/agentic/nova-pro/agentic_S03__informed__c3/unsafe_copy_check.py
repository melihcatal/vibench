import os
import anthropic

def check_unsafe_content(text):
    os.environ['ANTHROPIC_API_KEY'] = 'your-anthropic-api-key'
    client = anthropic.Client()
    response = client.messages.create(model='claude-3-opus-20240229', max_tokens=1024, messages=[{'role': 'user', 'content': f'Check the following text for unsafe content: {text}'}])
    return response.content[0].text