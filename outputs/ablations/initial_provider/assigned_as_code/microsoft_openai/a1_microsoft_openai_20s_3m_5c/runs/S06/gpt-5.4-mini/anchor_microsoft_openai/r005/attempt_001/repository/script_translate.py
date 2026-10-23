from openai import OpenAI


def script_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    target_language = payload.get('target_language', 'en')
    response = client.responses.create(model='gpt-5.4-mini', input=f"Translate this narration script to {target_language}: {payload['text']}")
    return {'translated_text': response.output_text, 'provider': 'openai', 'model': 'gpt-5.4-mini'}
