from typing import List
import os
import numpy as np
from openai import OpenAI
from .embeddings_client import get_embeddings_client
from .embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Generates embeddings for a batch of texts using OpenAI's embeddings API.

    Args:
        texts: List of input texts to embed.
        model: OpenAI embedding model to use. Defaults to "text-embedding-3-small".

    Returns:
        List[List[float]]: List of embedding vectors for the input texts.
    """
    client = get_embeddings_client()

    request = EmbeddingRequest(input=texts, model=model)
    response: EmbeddingResponse = client.embeddings.create(**request.dict())

    embeddings = [data.embedding for data in response.data]
    return embeddings
