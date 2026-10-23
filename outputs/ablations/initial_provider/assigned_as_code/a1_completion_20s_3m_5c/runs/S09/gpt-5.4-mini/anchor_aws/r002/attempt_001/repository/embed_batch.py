from embeddings_client import get_client, get_config, invoke_embedding
from embeddings_models import normalize_embedding_response


def embed_batch(payload, config=None):
    config = get_config(config)
    client = get_client(config)
    texts = payload["texts"]
    results = []
    for text in texts:
        raw = invoke_embedding(client, config["model_id"], {"inputText": text})
        results.append(normalize_embedding_response(raw))
    return {"embeddings": results}
