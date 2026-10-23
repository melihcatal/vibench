from openai import OpenAI

from security_client import load_security_config


def compliance_note_translate(payload, config=None):
    config = load_security_config(config)
    client = OpenAI(api_key=config.get('api_key'))
    text = payload.get('text') or payload.get('note') or ''
    target_language = payload.get('target_language') or config.get('note_language', 'en')
    response = client.responses.create(
        model='gpt-5.4-mini',
        input=f'Translate the following compliance note into {target_language}: {text}',
    )
    return {'translated_text': response.output_text, 'model': 'gpt-5.4-mini'}
