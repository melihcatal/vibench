from typing import List, Optional
import numpy as np
from openai import OpenAI
from .embeddings_client import get_embeddings_client
from .embeddings_models import EmbeddingRequest, EmbeddingResponse

client = get_embeddings_client()

MODEL_ID = "text-embedding-3-small"


def embed_batch(
    texts: List[str], dimensions: Optional[int] = None
) -> List[List[float]]:
    """Generate embeddings for a batch of texts using OpenAI's text-embedding-3-small model."""
    request = EmbeddingRequest(input=texts, model=MODEL_ID, dimensions=dimensions)
    response: EmbeddingResponse = client.embeddings.create(**request.dict())

    embeddings = [data.embedding for data in response.data]
    normalized_embeddings = [
        np.array(embedding) / np.linalg.norm(embedding) for embedding in embeddings
    ]
    return [embedding.tolist() for embedding in normalized_embeddings]
