from typing import List
from embeddings_client import get_gemini_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_query(query: str) -> List[float]:
    """Embeds a query for semantic search using Google Gemini Embeddings."""
    model = get_gemini_embeddings_client()
    response = model.embed_content(content=query, task_type="RETRIEVAL_QUERY")
    embedding_response = normalize_embedding_response(response)
    return embedding_response.embeddings[0]


def embed_documents(documents: List[str]) -> List[List[float]]:
    """Embeds documents for semantic search using Google Gemini Embeddings."""
    model = get_gemini_embeddings_client()
    response = model.embed_content(content=documents, task_type="RETRIEVAL_DOCUMENT")
    embedding_response = normalize_embedding_response(response)
    return embedding_response.embeddings
