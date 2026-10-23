from typing import List, Dict, Tuple

from embeddings_client import DashScopeEmbeddingsClient
from embeddings_models import BatchEmbeddingResponse


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[List[float], BatchEmbeddingResponse]:
    """
    Embed a query and a list of documents for semantic search using DashScope Text Embeddings.
    Requires DASHSCOPE_API_KEY environment variable.
    """
    client = DashScopeEmbeddingsClient()
    query_embedding = client.embed(query)
    doc_embeddings = client.batch_embed(documents)
    return query_embedding, BatchEmbeddingResponse(
        embeddings=doc_embeddings, model=client.model
    )
