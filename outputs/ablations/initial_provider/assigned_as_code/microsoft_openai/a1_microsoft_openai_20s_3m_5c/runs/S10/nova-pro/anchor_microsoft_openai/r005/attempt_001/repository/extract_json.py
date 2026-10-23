import os
from openai import OpenAI

def extract_json(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini',
            messages=[{'role': 'user', 'content': 'Extract the following text into structured JSON:

' + payload['text']}])
    return {'json': response.choices[0].message.content or ''}
