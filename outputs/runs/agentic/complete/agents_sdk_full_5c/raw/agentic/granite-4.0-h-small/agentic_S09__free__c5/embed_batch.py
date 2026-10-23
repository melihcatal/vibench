import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding, batch_normalize_embeddings

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of text strings using the Direct Embeddings API.
    """
    client = get_client()
    # Provider-specific payload construction (OpenAI example)
    response = client.create(
        model="text-embedding-ada-002",
        input=texts,
        dimensions=1536,
    )
    # Assume response['embeddings'] is a list of dicts each with an 'embedding' key
    embeddings = [emb.get('embedding', []) for emb in response.get('embeddings', [])]
    return batch_normalize_embeddings(embeddings)
