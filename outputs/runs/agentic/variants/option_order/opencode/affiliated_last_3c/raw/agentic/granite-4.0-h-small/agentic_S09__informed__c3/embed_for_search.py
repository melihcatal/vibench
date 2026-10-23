import os
from embeddings_client import get_embedder
from similarity_score import cosine_similarity


def embed_for_search(query: str, documents: list[str]) -> list[tuple[int, float]]:
    """Embed a query and a list of documents, then return ranked document indices by similarity.

    Args:
        query (str): The search query.
        documents (list[str]): List of document texts to search.

    Returns:
        list[tuple[int, float]]: Sorted list of (index, similarity_score) pairs.
    """
    client = get_embedder()
    query_embedding = client.embed_text([query])[0]
    doc_embeddings = client.embed_text(documents)

    scored_docs = []
    for idx, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scored_docs.append((idx, score))

    # Return sorted by highest similarity
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    return scored_docs
