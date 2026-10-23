import os

from openai import OpenAI

from vision_models import normalize_text


def visual_safety_text(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY'])
    text = normalize_text(payload.get('text'))
    response = client.responses.create(model='gpt-5.4-mini', input=f'Check this visual label text for unsafe or policy-sensitive content and answer with a short risk label: {text}')
    return {'risk_label': normalize_text(response.output_text)}
