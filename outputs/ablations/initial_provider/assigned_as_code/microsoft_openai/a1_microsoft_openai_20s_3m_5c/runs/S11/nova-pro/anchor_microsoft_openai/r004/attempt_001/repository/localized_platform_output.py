from openai import AzureOpenAI


def translate_platform_output(payload, config, target_language):
    client = AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21'))
    response = client.translations.create(model=config['deployment'], text=payload['text'], target_language=target_language)
    return response.text

