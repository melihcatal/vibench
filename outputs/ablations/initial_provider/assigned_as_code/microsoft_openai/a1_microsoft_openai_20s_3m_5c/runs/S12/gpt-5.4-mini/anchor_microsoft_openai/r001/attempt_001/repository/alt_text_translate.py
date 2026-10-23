from openai import OpenAI


def alt_text_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('openai_api_key'))
    text = payload.get('text', '')
    target_language = payload.get('target_language', 'es')
    prompt = f'Translate the image description into {target_language}.'
    result = client.responses.create(model=config.get('model', 'gpt-4.1-mini'), input=[{'role': 'system', 'content': prompt}, {'role': 'user', 'content': text}])
    return {'translation': result.output_text}
