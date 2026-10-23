def summarize_embedding_job(results: list[tuple[str, float]]) -> str:
    """Create a concise summary of embedding job results.

    Args:
        results: List of (document_text, similarity_score) tuples.

    Returns:
        A multi-line string summarizing key statistics and top matches.
    """
    if not results:
        return "No results returned from embedding job."
    summary = ["Embedding job summary:", f"Total matches: {len(results)}"]
    # Statistics
    scores = [score for _, score in results]
    summary.append(f"Min similarity: {min(scores):.4f}")
    summary.append(f"Max similarity: {max(scores):.4f}")
    summary.append(f"Avg similarity: {sum(scores) / len(scores):.4f}")
    # Top 3 matches
    top_matches = results[:3]
    summary.append("Top matches:")
    for doc, score in top_matches:
        summary.append(f"  - {doc[:80]}... (score: {score:.4f})")
    return "\n".join(summary)
