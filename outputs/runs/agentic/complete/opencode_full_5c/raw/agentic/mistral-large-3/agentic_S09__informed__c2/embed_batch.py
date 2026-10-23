from typing import List

from embeddings_client import DashScopeEmbeddingsClient
from embeddings_models import BatchEmbeddingResponse


def embed_batch(texts: List[str]) -> BatchEmbeddingResponse:
    """
    Generate embeddings for a batch of texts using DashScope Text Embeddings.
    Requires DASHSCOPE_API_KEY environment variable.
    """
    client = DashScopeEmbeddingsClient()
    embeddings = client.batch_embed(texts)
    return BatchEmbeddingResponse(embeddings=embeddings, model=client.model)
