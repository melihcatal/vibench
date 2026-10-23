from openai import AzureOpenAI


def localized_platform_output(payload, config=None):
    config = config or {}
    locale = config.get('locale', 'es')
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.chat.completions.create(model=config['deployment'], messages=[{'role': 'user', 'content': f"Translate to {locale}: {payload['text']}"}])
    return {'text': response.choices[0].message.content or '', 'locale': locale}
