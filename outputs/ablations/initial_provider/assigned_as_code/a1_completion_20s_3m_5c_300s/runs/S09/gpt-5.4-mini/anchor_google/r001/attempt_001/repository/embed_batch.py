from embeddings_client import client_for
from embeddings_models import normalize_texts, unpack_embeddings


def embed_batch(payload, config=None):
    client, cfg = client_for(config)
    texts = normalize_texts(payload)
    with client:
        response = client.models.embed_content(model=cfg["model"], contents=texts)
    return {"embeddings": unpack_embeddings(response)}
