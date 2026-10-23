from typing import List, Dict, Any
from .embed_text import embed_text
from .embed_batch import embed_batch


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Embeds a query and a list of documents for semantic search using OpenAI's embeddings API.

    Args:
        query: Input query text to embed.
        documents: List of document texts to embed.
        model: OpenAI embedding model to use. Defaults to "text-embedding-3-small".

    Returns:
        Dict[str, Any]: A dictionary containing the query embedding and document embeddings.
    """
    query_embedding = embed_text(query, model=model)
    document_embeddings = embed_batch(documents, model=model)

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
        "documents": documents,
    }
