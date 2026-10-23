import os
from model_client import get_openai_client

def stream_completion(payload, config=None):
    config = config or {}
    client = get_openai_client(config.get('api_key'))
    stream = client.chat.completions.create(
        model='gpt-5.4-mini',
        messages=[
            {'role': 'user', 'content': payload['prompt']}
        ],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield {'token': chunk.choices[0].delta.content}
