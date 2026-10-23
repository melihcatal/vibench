from typing import List, Optional
import os
import numpy as np
from openai import OpenAI
from .embeddings_client import get_embeddings_client
from .embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generates an embedding vector for a single text string using OpenAI's embeddings API.

    Args:
        text: Input text to embed.
        model: OpenAI embedding model to use. Defaults to "text-embedding-3-small".

    Returns:
        List[float]: Embedding vector for the input text.
    """
    client = get_embeddings_client()

    request = EmbeddingRequest(input=text, model=model)
    response: EmbeddingResponse = client.embeddings.create(**request.dict())

    embedding = response.data[0].embedding
    return embedding
