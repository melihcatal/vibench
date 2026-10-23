# embed_batch.py
import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import check_response

def embed_batch(texts: list[str]):
    """Generate embeddings for a batch of texts using Direct Embeddings API.

    Args:
        texts (list[str]): list of input strings.

    Returns:
        list[list[float]]: list of embedding vectors.
    """
    client = DirectEmbeddingsClient()
    response = client.create_embedding(
        input=texts,
        model="text-embedding-ada-002"  # concrete model identifier
    )
    check_response(response)
    return [item['embedding'] for item in response['data']]
