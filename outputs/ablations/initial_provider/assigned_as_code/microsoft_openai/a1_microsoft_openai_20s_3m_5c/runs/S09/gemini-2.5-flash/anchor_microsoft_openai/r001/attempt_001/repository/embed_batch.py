from embeddings_client import EmbeddingsClient
from embeddings_models import EMBEDDING_MODEL

def embed_batch(payload, config=None):
    client = EmbeddingsClient(api_key=config.get('api_key') if config else None).get_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=payload['texts'])
    return {'embeddings': [item.embedding for item in response.data]}
