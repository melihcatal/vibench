from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    client = OpenAIClient(endpoint=config['openai_endpoint'], credential=AzureKeyCredential(config['openai_key']))
    text = payload.get('text', '')
    model = config.get('model', 'text-embedding-3-large')
    response = client.get_embeddings(model=model, input=[text])
    embedding = response.data[0].embedding if response.data else []
    return {'embedding': embedding, 'model': model, 'source': 'azure-openai'}
