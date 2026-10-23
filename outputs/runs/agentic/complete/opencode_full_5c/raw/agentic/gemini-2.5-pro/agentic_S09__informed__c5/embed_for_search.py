from embeddings_client import get_embeddings_client
from typing import List, Dict, Any


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    """
    Embeds a query and documents for semantic search using Gemini API.
    """
    client = get_embeddings_client()

    query_result = client.embed_content(
        model="models/embedding-001", content=query, task_type="retrieval_query"
    )

    docs_result = client.embed_content(
        model="models/embedding-001", content=documents, task_type="retrieval_document"
    )

    return {
        "query_embedding": query_result["embedding"],
        "document_embeddings": [embedding for embedding in docs_result["embedding"]],
    }
