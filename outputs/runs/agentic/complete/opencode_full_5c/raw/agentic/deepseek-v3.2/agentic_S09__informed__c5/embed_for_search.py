import os
from typing import List, Tuple
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_text


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and documents for semantic search."""
    client = get_embeddings_client()

    normalized_query = normalize_text(query)
    normalized_docs = [normalize_text(doc) for doc in documents]

    all_texts = [normalized_query] + normalized_docs

    response = client.embeddings.create(model=model, input=all_texts)

    query_embedding = response.data[0].embedding
    document_embeddings = [item.embedding for item in response.data[1:]]

    return query_embedding, document_embeddings
