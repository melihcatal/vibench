import os
from embeddings_client import get_gemini_client, get_embedding_model_name
from embeddings_models import normalize_embedding_response
from typing import List, Dict, Any


def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[List[float]]]:
    """Embeds a query and documents for semantic search using Google Gemini Embeddings."""
    genai = get_gemini_client()
    model_name = get_embedding_model_name()

    query_embedding_response = genai.embed_content(
        model=model_name, content=query, task_type="RETRIEVAL_QUERY"
    )
    query_embedding = normalize_embedding_response(query_embedding_response)[0]

    document_embeddings_response = genai.embed_content(
        model=model_name, content=documents, task_type="RETRIEVAL_DOCUMENT"
    )
    document_embeddings = normalize_embedding_response(document_embeddings_response)

    return {
        "query_embedding": [query_embedding],
        "document_embeddings": document_embeddings,
    }
