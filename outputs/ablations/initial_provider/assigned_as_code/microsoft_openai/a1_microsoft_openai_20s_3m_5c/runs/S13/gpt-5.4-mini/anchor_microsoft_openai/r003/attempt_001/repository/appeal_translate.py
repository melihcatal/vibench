from openai import OpenAI


def appeal_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    text = payload.get('text', '') if isinstance(payload, dict) else str(payload)
    target = (payload.get('target_language') if isinstance(payload, dict) else None) or 'English'
    response = client.responses.create(model='gpt-5.4-mini', input=f'Translate this appeal text into {target}: {text}')
    return {'translation': response.output_text}
