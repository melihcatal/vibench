import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of texts using the Direct Embeddings API.

    Args:
        texts: List of strings, each to be embedded.

    Returns:
        List of embedding vectors (each a list of floats) in the same order as the input.
    """
    client = get_client()
    model_id = "text-embedding-ada-002"  # provider-specific model identifier
    response = client.create_embedding(
        model=model_id,
        input=texts,
        # optional parameters such as batch size control can be added here
    )
    # Assume the API returns a list of embeddings under the key 'embeddings'
    embeddings = response["embeddings"]
    return [normalize_embedding(vec) for vec in embeddings]
