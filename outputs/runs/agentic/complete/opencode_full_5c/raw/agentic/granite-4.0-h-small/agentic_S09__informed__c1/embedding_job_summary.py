# [LATER-STEP] embedding_job_summary.py
# Summarize results of an embedding job (e.g., search, batch embed)

from typing import List, Tuple


def summarize_embedding_job(
    query_embedding: list[float],
    doc_embeddings: List[list[float]],
    similarities: List[float],
) -> str:
    """Create a concise textual summary of embedding job results.

    Includes query ID, number of docs, and top‑k similarity stats.

    Args:
        query_embedding (list[float]): Embedding of the query.
        doc_embeddings (List[list[float]]): Embeddings of the documents.
        similarities (List[float]): Cosine similarities for each document.

    Returns:
        str: Human‑readable summary.
    """
    n_docs = len(doc_embeddings)
    top_k = min(5, n_docs)
    top_similarities = sorted(similarities, reverse=True)[:top_k]
    summary = (
        f"Embedding job summary:\n"
        f"- Query vector length: {len(query_embedding)}\n"
        f"- Documents processed: {n_docs}\n"
        f"- Top {top_k} similarity scores: {top_similarities}\n"
    )
    return summary
