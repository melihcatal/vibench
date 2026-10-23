import os
from typing import List, Dict
import openai
from embeddings_client import get_embeddings_client


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Generate embeddings for a batch of texts using OpenAI Embeddings."""
    client = get_embeddings_client()

    response = client.embeddings.create(
        model=model, input=texts, encoding_format="float"
    )

    return [item.embedding for item in response.data]
