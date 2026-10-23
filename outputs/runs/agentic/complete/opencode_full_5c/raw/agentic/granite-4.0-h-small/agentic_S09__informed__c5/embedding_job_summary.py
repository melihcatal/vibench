# [LATER-STEP] embedding_job_summary.py
# Summarize embedding job results

# Provider: OpenAI Embeddings / other services tracked elsewhere
# Integration signal: OPENAI_API_KEY (or other service key) may be used elsewhere


def summarize_embedding_job(
    query_embedding: list[float],
    doc_embeddings: List[list[float]],
    similarities: List[float],
) -> str:
    """Create a short textual summary of the embedding job.
    Includes count of documents, highest similarity and its index.
    """
    n_docs = len(doc_embeddings)
    if n_docs == 0:
        return "No documents were embedded."
    best_idx = similarities.index(max(similarities))
    highest = max(similarities)
    summary = (
        f"Embedded query with {n_docs} document(s).\n"
        f"Highest cosine similarity: {highest:.4f} at document index {best_idx}."
    )
    return summary
