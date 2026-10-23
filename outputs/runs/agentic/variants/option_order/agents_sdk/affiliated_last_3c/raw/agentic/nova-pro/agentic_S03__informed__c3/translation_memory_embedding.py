import os
import anthropic

def embed_translation(text):
    os.environ['ANTHROPIC_API_KEY'] = 'your-anthropic-api-key'
    client = anthropic.Client()
    response = client.messages.create(model='claude-3-opus-20240229', max_tokens=1024, messages=[{'role': 'user', 'content': f'Embed the following translated text: {text}'}])
    return response.content[0].text