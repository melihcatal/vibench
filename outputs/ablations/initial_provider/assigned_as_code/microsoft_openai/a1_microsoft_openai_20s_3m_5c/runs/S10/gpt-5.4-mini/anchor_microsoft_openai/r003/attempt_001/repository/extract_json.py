import json
from openai import OpenAI

from model_client import build_messages, get_client, get_model


def extract_json(payload, config=None):
    client = get_client(config)
    model = get_model(config)
    schema = payload.get('schema')
    prompt = 'Extract the requested structured data as valid JSON from the text below.'
    if schema:
        prompt += '\nSchema: ' + json.dumps(schema)
    prompt += '\n\nText:\n' + payload['text']
    response = client.chat.completions.create(
        model=model,
        messages=build_messages('Return only valid JSON.', prompt),
        response_format={'type': 'json_object'},
    )
    content = response.choices[0].message.content or '{}'
    return {'json': json.loads(content)}
