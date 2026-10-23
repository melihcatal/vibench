from openai import AzureOpenAI


def ocr_embedding(payload, config=None):
    config = config or {}
    client = AzureOpenAI(api_key=config['embedding_key'], azure_endpoint=config['embedding_endpoint'], api_version='2024-02-15-preview')
    response = client.embeddings.create(model=config['embedding_model'], input=payload.get('sections', []))
    return {'embeddings': [item.embedding for item in response.data]}
