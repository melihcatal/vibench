from openai import AzureOpenAI


def platform_output_embedding(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.embeddings.create(model=config.get('embedding_deployment', config.get('deployment')), input=payload['text'])
    return {'embedding': response.data[0].embedding, 'model': response.model}
