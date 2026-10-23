from typing import List, Optional
import os
import numpy as np
from openai import OpenAI
from .embeddings_client import get_embeddings_client
from .embeddings_models import EmbeddingRequest, EmbeddingResponse

client = get_embeddings_client()

MODEL_ID = "text-embedding-3-small"


def embed_text(text: str, dimensions: Optional[int] = None) -> List[float]:
    """Generate an embedding vector for a single text string using OpenAI's text-embedding-3-small model."""
    request = EmbeddingRequest(input=text, model=MODEL_ID, dimensions=dimensions)
    response: EmbeddingResponse = client.embeddings.create(**request.dict())

    embedding = response.data[0].embedding
    normalized_embedding = np.array(embedding) / np.linalg.norm(embedding)
    return normalized_embedding.tolist()
