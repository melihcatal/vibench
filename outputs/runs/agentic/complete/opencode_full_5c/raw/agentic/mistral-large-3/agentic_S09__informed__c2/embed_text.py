import os
from typing import List, Optional

from embeddings_client import DashScopeEmbeddingsClient
from embeddings_models import EmbeddingResponse


def embed_text(text: str) -> Optional[EmbeddingResponse]:
    """
    Generate an embedding vector for a single text string using DashScope Text Embeddings.
    Requires DASHSCOPE_API_KEY environment variable.
    """
    client = DashScopeEmbeddingsClient()
    embedding = client.embed(text)
    if embedding:
        return EmbeddingResponse(embedding=embedding, model=client.model)
    return None
