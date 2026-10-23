import os
import anthropic

def summarize_quality(text):
    os.environ['ANTHROPIC_API_KEY'] = 'your-anthropic-api-key'
    client = anthropic.Client()
    response = client.messages.create(model='claude-3-opus-20240229', max_tokens=1024, messages=[{'role': 'user', 'content': f'Summarize the translation quality issues in the following text: {text}'}])
    return response.content[0].text