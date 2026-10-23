import os
from openai import OpenAI


def answer_with_context(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini',
            messages=[{'role': 'user', 'content': 'Answer the following question using the provided context:

Question: ' + payload['question'] + '

Context: ' + payload['context']}])
    return {'answer': response.choices[0].message.content or ''}