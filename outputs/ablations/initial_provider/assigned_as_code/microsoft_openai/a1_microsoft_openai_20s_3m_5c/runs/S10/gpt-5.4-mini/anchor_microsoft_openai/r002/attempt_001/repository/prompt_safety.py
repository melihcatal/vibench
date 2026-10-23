from openai import OpenAI
from model_client import get_config, get_model


def prompt_safety(payload, config=None):
    resolved = get_config(config)
    text = payload.get('text') or payload.get('prompt') or ''
    with OpenAI(api_key=resolved['api_key']) as client:
        response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': 'Classify whether the following content is unsafe. Return a short verdict and reason.\n\n' + text}])
    return {'text': response.choices[0].message.content or ''}
