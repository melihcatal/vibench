from openai import AzureOpenAI


def embed_platform_output(payload, config):
    client = AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21'))
    response = client.embeddings.create(model=config['deployment'], input=payload['text'])
    return response.data[0].embedding

