import os

from openai import OpenAI

from vision_models import normalize_text


def alt_text_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY'])
    target_language = normalize_text(config.get('target_language') or 'Spanish')
    description = normalize_text(payload.get('description'))
    response = client.responses.create(model='gpt-5.4-mini', input=f'Translate this image description into {target_language}: {description}')
    return {'translated_description': normalize_text(response.output_text)}
