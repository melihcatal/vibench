from embed_text import embed_text
from embeddings_client import get_embedder


def embed_for_search(query: str, document_texts: list[str]) -> list[tuple[str, float]]:
    """Embed a query and a list of documents, then compute similarity scores.

    Args:
        query (str): The search query text.
        document_texts (list[str]): List of document texts to compare against.

    Returns:
        list[tuple[str, float]]: Sorted list of (document_text, similarity_score) pairs.
    """
    query_embedding = embed_text(query)
    doc_embeddings = [embed_text(doc) for doc in document_texts]
    scored_docs = []
    for doc_text, doc_emb in zip(document_texts, doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scored_docs.append((doc_text, score))
    # Sort by descending similarity
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    return scored_docs
