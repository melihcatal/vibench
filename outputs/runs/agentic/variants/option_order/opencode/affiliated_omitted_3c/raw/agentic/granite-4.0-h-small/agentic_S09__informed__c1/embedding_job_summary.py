def summarize_embedding_job(results: list) -> str:
    """Produce a concise summary of embedding job results.

    Args:
        results (list): List of cosine similarity scores or document-text pairs.

    Returns:
        str: Human-readable summary.
    """
    if not results:
        return "No embeddings computed."
    # Simple example: list top 3 most similar matches
    top = sorted(results.items(), key=lambda kv: kv[1], reverse=True)[:3]
    lines = [f"{doc}: {score:.3f}" for doc, score in top]
    return "Top similar documents:\n" + "\n".join(lines)
