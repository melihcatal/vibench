from typing import List, Dict, Tuple
from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingResponse


def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and documents for semantic search using Cohere Embed API."""
    client = get_cohere_client()
    texts = [query] + documents
    response = client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_query" if len(texts) == 1 else "search_document"
    )
    embedding_response = EmbeddingResponse(response)
    query_embedding = embedding_response.embeddings[0]
    document_embeddings = embedding_response.embeddings[1:]
    return query_embedding, document_embeddings