import os
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def extract_json(text):
    response = client.messages.create(model='claude-3-opus-20240229', max_tokens=1024, messages=[{"role": "user", "content": text}])
    return response.content[0].text
