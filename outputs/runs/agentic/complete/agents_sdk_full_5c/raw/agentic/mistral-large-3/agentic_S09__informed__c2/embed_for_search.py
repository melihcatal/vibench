from typing import List, Dict, Any

from embed_text import embed_text
from embed_batch import embed_batch


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    """Embed query and documents for semantic search using DashScope."""
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)
    
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
        "documents": documents
    }