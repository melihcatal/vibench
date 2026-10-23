from embeddings_client import get_client, get_model
from embeddings_models import normalize_texts


def embed_batch(payload, config=None):
    config = config or {}
    texts = normalize_texts(payload)
    with get_client(config) as client:
        response = client.embeddings.create(model=get_model(config), input=texts)
    return {'embeddings': [item.embedding for item in response.data]}
