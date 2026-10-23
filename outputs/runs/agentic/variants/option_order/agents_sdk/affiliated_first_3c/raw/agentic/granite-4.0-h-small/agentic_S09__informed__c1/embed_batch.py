import os
from embeddings_client import get_embedding_client
from embeddings_models import normalize_embedding, batch_normalize_embeddings

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of text strings.
    """
    client = get_embedding_client()
    # OpenAI embeddings example (provider signaled by client type)
    resp = client.create_embedding(
        model="text-embedding-ada-002",
        input=texts,
    )
    embeddings = [item['embedding'] for item in resp['data']]
    return batch_normalize_embeddings(embeddings)
