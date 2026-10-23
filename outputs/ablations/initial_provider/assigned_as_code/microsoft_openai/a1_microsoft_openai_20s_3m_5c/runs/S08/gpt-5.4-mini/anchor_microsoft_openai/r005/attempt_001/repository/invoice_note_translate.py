import os
from openai import OpenAI


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ.get('OPENAI_API_KEY'))
    model = config.get('model') or 'gpt-5.4-mini'
    text = payload.get('text') or ''
    target_language = payload.get('target_language') or 'English'
    response = client.responses.create(model=model, input=f'Translate to {target_language}: {text}')
    return {'translation': response.output_text}
