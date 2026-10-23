from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential


def log_embedding(payload, config=None):
    config = config or {}
    client = EmbeddingsClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    text = str(payload.get('text', ''))
    result = client.embed(input=[text], model=config.get('model', 'text-embedding-3-large'))
    vector = result.data[0].embedding if result and result.data else []
    return {'embedding': vector, 'dimension': len(vector)}
