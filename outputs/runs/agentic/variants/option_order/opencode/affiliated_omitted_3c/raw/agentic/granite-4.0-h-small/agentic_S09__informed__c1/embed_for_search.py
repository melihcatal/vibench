import os
from embeddings_client import get_embedder
from similarity_score import cosine_similarity


def embed_for_search(query: str, documents: list) -> dict:
    """Embed a query and a list of documents for semantic search.

    Args:
        query (str): The search query text.
        documents (list): A list of document texts to be embedded.

    Returns:
        dict: Mapping of document text to similarity score against the query.
    """
    query_emb = get_embedder().embed_text(query)
    doc_embeddings = get_embedder().embed_batch(documents)
    results = {}
    for doc, emb in zip(documents, doc_embeddings):
        sim = cosine_similarity(query_emb, emb)
        results[doc] = sim
    return results
