import os
from anthropic import Anthropic

os.environ['ANTHROPIC_API_KEY'] = 'your-anthropic-api-key'

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def summarize_message(message):
    response = client.messages.create(model='claude-3-opus-20240229', max_tokens=1024, messages=[{"role": "user", "content": message}])
    return response.content