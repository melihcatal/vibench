from embeddings_client import DirectEmbeddingsClient


def embed_batch(texts, config=None):
    client = DirectEmbeddingsClient(config)
    payload = {"texts": texts}
    response = client.embed_batch(payload)
    return {"embeddings": response['embeddings']}