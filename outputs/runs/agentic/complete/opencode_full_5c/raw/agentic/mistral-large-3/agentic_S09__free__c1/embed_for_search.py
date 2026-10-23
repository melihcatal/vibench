from typing import List, Dict
from .embed_text import embed_text
from .similarity_score import similarity_score


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Dict[str, List[float]]:
    """
    Embeds a query and a list of documents for semantic search using OpenAI's Embeddings API.

    Args:
        query: Input query text.
        documents: List of document texts to compare against the query.
        model: OpenAI embedding model identifier.

    Returns:
        Dictionary containing the query embedding and document embeddings.
    """
    query_embedding = embed_text(query, model=model)
    document_embeddings = [embed_text(doc, model=model) for doc in documents]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }


def search_documents(
    query: str,
    documents: List[str],
    top_k: int = 3,
    model: str = "text-embedding-3-small",
) -> List[Dict[str, float]]:
    """
    Performs semantic search on documents based on a query.

    Args:
        query: Input query text.
        documents: List of document texts to search.
        top_k: Number of top results to return.
        model: OpenAI embedding model identifier.

    Returns:
        List of dictionaries containing document indices and their similarity scores.
    """
    embeddings = embed_for_search(query, documents, model=model)
    query_embedding = embeddings["query_embedding"]
    document_embeddings = embeddings["document_embeddings"]

    scores = [
        {"index": idx, "score": similarity_score(query_embedding, doc_embedding)}
        for idx, doc_embedding in enumerate(document_embeddings)
    ]

    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:top_k]
