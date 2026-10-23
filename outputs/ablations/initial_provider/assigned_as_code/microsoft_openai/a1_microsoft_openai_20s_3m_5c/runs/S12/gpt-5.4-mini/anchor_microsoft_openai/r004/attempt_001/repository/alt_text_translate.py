from openai import OpenAI


def alt_text_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    model = config.get('model', 'gpt-4.1-mini')
    source = payload.get('text', '')
    target_language = payload.get('target_language', 'English')
    prompt = f'Translate the following image alt text into {target_language} while preserving meaning: {source}'
    response = client.responses.create(model=model, input=[{'role': 'user', 'content': prompt}])
    return {'translation': response.output_text}
