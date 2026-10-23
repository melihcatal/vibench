import os
from openai import OpenAI

def stream_completion(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini',
            messages=[{'role': 'user', 'content': payload['text']}],
            stream=True)
        for chunk in response:
            yield chunk.choices[0].delta.content or ''
