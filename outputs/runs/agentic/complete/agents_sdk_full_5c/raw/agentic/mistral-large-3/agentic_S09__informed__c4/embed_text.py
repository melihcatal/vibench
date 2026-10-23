import os
from typing import List

from embeddings_client import get_embeddings_client, get_embedding_model
from embeddings_models import normalize_embedding, parse_embedding_response


def embed_text(text: str, normalize: bool = True) -> List[float]:
    """
    Generate an embedding vector for a single text string using OpenAI embeddings.
    
    Args:
        text: Input text string.
        normalize: Whether to normalize the embedding to unit length.
    
    Returns:
        Embedding vector as a list of floats.
    """
    client = get_embeddings_client()
    model = get_embedding_model()

    response = client.embeddings.create(input=text, model=model)
    embedding = parse_embedding_response(response.model_dump())

    if normalize:
        embedding = normalize_embedding(embedding)
    return embedding