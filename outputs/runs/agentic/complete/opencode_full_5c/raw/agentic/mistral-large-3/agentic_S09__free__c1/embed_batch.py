from typing import List
import numpy as np
from openai import OpenAI
from .embeddings_client import get_embeddings_client
from .embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Generates embeddings for a batch of texts using OpenAI's Embeddings API.

    Args:
        texts: List of input texts to embed.
        model: OpenAI embedding model identifier.

    Returns:
        List of embedding vectors, each as a list of floats.
    """
    client = get_embeddings_client()
    request = EmbeddingRequest(input=texts, model=model)

    response = client.embeddings.create(input=request.input, model=request.model)

    embedding_response = EmbeddingResponse(**response.model_dump())
    return [item.embedding for item in embedding_response.data]
