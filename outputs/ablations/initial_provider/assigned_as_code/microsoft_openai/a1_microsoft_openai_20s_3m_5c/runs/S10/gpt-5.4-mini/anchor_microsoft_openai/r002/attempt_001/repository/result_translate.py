from openai import OpenAI
from model_client import get_config, get_model


def result_translate(payload, config=None):
    resolved = get_config(config)
    target_language = payload.get('target_language') or 'English'
    text = payload.get('text') or ''
    prompt = 'Translate the following model output into ' + target_language + '. Preserve meaning and formatting.\n\n' + text
    with OpenAI(api_key=resolved['api_key']) as client:
        response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}])
    return {'text': response.choices[0].message.content or ''}
