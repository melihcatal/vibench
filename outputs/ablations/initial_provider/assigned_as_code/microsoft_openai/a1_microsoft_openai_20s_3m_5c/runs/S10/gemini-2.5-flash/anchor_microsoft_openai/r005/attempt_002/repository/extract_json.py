import os
from model_client import get_openai_client

def extract_json(payload, config=None):
    config = config or {}
    client = get_openai_client(config.get('api_key'))
    response = client.chat.completions.create(
        model='gpt-5.4-mini',
        response_format={'type': 'json_object'},
        messages=[
            {'role': 'system', 'content': 'You are an AI assistant that extracts structured JSON from text.'},
            {'role': 'user', 'content': 'Extract JSON from the following text:\n\n' + payload['text']}
        ]
    )
    return {'json_data': response.choices[0].message.content or '{}'}
