import os
from anthropic import Anthropic

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

client = Anthropic(api_key=anthropic_api_key)

def archive_summary(text):
    response = client.messages.create(model='claude-3-opus-20240229', max_tokens=1024, messages=[{"role": "user", "content": f"Summarize the following text: {text}"}])
    return response.content[0].text