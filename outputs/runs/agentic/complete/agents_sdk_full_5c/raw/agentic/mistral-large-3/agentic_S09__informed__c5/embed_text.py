import os
from typing import List
import numpy as np
from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingResponse


def embed_text(text: str) -> List[float]:
    """Generate an embedding vector for a single text string using Cohere Embed API."""
    client = get_cohere_client()
    response = client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embedding_response = EmbeddingResponse(response)
    return embedding_response.embeddings[0]