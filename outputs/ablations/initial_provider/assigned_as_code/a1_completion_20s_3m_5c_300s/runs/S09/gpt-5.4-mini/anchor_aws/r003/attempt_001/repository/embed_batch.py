from embeddings_client import create_client, invoke_batch_embeddings
from embeddings_models import normalize_texts


def embed_batch(payload, config=None):
    client, cfg = create_client(config)
    texts = normalize_texts(payload["texts"])
    return {"embeddings": invoke_batch_embeddings(client, cfg["model_id"], texts)}
