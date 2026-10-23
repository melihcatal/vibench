import os
from openai import OpenAI


def summarize_text(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini',
            messages=[{'role': 'user', 'content': 'Summarize the following text concisely:\n\n' + payload['text']}])
    return {'text': response.choices[0].message.content or ''}
