from embed_text import embed_text
from embed_batch import embed_batch


def embed_for_search(query: str, documents: list[str]) -> dict:
    """Embeds a query and a list of documents for semantic search."""
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
