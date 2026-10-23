from typing import List

from embeddings_client import get_embeddings_client, get_embedding_model
from embeddings_models import normalize_embedding, parse_batch_embedding_response


def embed_batch(texts: List[str], normalize: bool = True) -> List[List[float]]:
    """
    Generate embeddings for a batch of text strings using OpenAI embeddings.
    
    Args:
        texts: List of input text strings.
        normalize: Whether to normalize each embedding to unit length.
    
    Returns:
        List of embedding vectors.
    """
    client = get_embeddings_client()
    model = get_embedding_model()

    response = client.embeddings.create(input=texts, model=model)
    embeddings = parse_batch_embedding_response(response.model_dump())

    if normalize:
        embeddings = [normalize_embedding(emb) for emb in embeddings]
    return embeddings