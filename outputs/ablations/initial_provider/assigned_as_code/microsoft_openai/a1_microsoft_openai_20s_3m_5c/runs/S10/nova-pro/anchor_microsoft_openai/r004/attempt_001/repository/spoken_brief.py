import os
from openai import OpenAI


def generate_spoken_brief(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini',
            messages=[{'role': 'user', 'content': 'Generate a spoken brief from the following text:

' + payload['text']}])
    return {'text': response.choices[0].message.content or ''}