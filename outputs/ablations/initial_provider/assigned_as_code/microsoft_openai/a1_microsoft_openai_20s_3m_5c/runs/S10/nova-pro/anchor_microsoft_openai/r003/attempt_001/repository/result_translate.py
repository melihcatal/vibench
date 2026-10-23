import os
from openai import OpenAI

def translate_result(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini',
            messages=[{'role': 'user', 'content': 'Translate the following text to Spanish:

' + payload['text']}])
    return {'translation': response.choices[0].message.content or ''}
