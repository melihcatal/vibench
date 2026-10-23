from openai import AzureOpenAI

def stream_platform_generation(payload, config):
    client = AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21'))
    response = client.chat.completions.create(model=config['deployment'], messages=[{'role': 'user', 'content': payload['text']}], stream=True)
    for chunk in response:
        yield chunk