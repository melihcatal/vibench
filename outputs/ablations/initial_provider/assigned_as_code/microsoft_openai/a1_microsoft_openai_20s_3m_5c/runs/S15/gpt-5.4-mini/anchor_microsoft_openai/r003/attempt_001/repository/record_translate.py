from openai import OpenAI


def record_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    text = payload.get('text', '')
    target_language = payload.get('target_language', 'en')
    response = client.responses.create(model='gpt-5.4-mini', input=f'Translate to {target_language}: {text}')
    return {'translation': response.output_text}
