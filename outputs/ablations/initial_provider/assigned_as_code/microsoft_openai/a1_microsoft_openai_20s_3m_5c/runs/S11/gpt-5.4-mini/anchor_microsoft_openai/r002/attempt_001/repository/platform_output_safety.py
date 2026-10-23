from openai import AzureOpenAI


def platform_output_safety(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.chat.completions.create(model=config['deployment'], messages=[{'role': 'user', 'content': payload['text']}])
    text = response.choices[0].message.content or ''
    unsafe = any(token in text.lower() for token in ['harm', 'weapon', 'explosive'])
    return {'text': text, 'unsafe': unsafe}
