from typing import List, Dict, Any
from embeddings_client import get_embeddings_client
from embeddings_models import (
    EMBEDDING_MODEL,
    TASK_TYPE_RETRIEVAL_QUERY,
    TASK_TYPE_RETRIEVAL_DOCUMENT,
)

def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    """
    Embeds a query and a list of documents for semantic search.

    Args:
        query: The search query.
        documents: A list of documents to be searched.

    Returns:
        A dictionary containing the query embedding and document embeddings.
    """
    genai = get_embeddings_client()

    # Embed the query
    query_embedding = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=query,
        task_type=TASK_TYPE_RETRIEVAL_QUERY
    )['embedding']

    # Embed the documents
    document_embeddings = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=documents,
        task_type=TASK_TYPE_RETRIEVAL_DOCUMENT
    )['embedding']

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
