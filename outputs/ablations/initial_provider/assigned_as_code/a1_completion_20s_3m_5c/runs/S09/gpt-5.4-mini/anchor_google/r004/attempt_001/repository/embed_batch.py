from embeddings_client import get_client, get_model
from embeddings_models import normalize_texts


def embed_batch(payload, config=None):
    config = config or {}
    texts = normalize_texts(payload)
    with get_client(config) as client:
        response = client.models.embed_content(model=get_model(config), contents=texts)
    return {"embeddings": [list(item.values) for item in response.embeddings]}
