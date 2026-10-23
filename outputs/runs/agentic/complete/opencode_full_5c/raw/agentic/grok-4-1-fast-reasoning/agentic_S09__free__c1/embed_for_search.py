from typing import List, Tuple
from embeddings_client import get_embedding, get_embeddings


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]]]:
    query_embedding = get_embedding(query, model="text-embedding-3-small")
    document_embeddings = get_embeddings(documents, model="text-embedding-3-small")
    return query_embedding, document_embeddings
