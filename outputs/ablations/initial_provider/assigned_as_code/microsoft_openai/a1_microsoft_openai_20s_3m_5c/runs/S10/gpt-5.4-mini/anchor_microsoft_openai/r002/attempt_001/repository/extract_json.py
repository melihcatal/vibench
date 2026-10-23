from openai import OpenAI
from model_client import get_config, get_model


def extract_json(payload, config=None):
    resolved = get_config(config)
    with OpenAI(api_key=resolved['api_key']) as client:
        response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': 'Extract the relevant structured JSON from the following text and return only valid JSON:\n\n' + payload['text']}], response_format={'type': 'json_object'})
    return {'json': response.choices[0].message.content or '{}'}
