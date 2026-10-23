from openai import AzureOpenAI


def asset_metadata_embedding(payload, config=None):
    config = config or {}
    client = AzureOpenAI(azure_endpoint=config['openai_endpoint'], api_key=config['openai_key'], api_version=config.get('openai_api_version', '2024-02-15-preview'))
    text = f"{payload.get('object_name', '')} {payload.get('metadata', {})} {payload.get('text', '')}".strip()
    response = client.embeddings.create(model=config['embedding_deployment'], input=text)
    return {'embedding': response.data[0].embedding}
