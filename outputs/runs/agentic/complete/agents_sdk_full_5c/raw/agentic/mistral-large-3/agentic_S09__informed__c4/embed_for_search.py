from typing import List, Dict, Any

from embed_text import embed_text


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    """
    Embed a query and a list of documents for semantic search using OpenAI embeddings.
    
    Args:
        query: Search query text.
        documents: List of document texts.
    
    Returns:
        Dictionary containing query embedding and document embeddings.
    """
    query_embedding = embed_text(query)
    document_embeddings = [embed_text(doc) for doc in documents]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
        "documents": documents,
    }