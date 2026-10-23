import os
from typing import List, Tuple, Dict, Any
from embeddings_client import get_embeddings_client


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Tuple[List[float], List[List[float]]]:
    """
    Embed a query and documents for semantic search using OpenAI Embeddings.

    Args:
        query: The search query string
        documents: List of document strings to search against
        model: The OpenAI embedding model identifier

    Returns:
        Tuple[List[float], List[List[float]]]: Query embedding and document embeddings
    """
    client = get_embeddings_client()

    # Embed query
    query_response = client.embeddings.create(model=model, input=query)
    query_embedding = query_response.data[0].embedding

    # Embed documents
    if documents:
        docs_response = client.embeddings.create(model=model, input=documents)
        doc_embeddings = [item.embedding for item in docs_response.data]
    else:
        doc_embeddings = []

    return query_embedding, doc_embeddings
