from typing import List, Tuple

def summarize_embedding_job(results: List[Tuple[str, float]]) -> str:
    """Produce a concise textual summary of embedding job outcomes.

    Args:
        results (List[Tuple[str, float]]): List of (document_text, similarity_score) pairs.

    Returns:
        str: Human-readable summary highlighting top matches.
    """
    if not results:
        return 'No documents were provided for comparison.'
    summary_lines = ['Embedding comparison results:']
    top_n = min(5, len(results))
    for i, (doc, score) in enumerate(results[:top_n], start=1):
        summary_lines.append(f\"{i}. Document: {doc}\" \
                              f\"Score: {score:.4f}\")
    return '\\n'.join(summary_lines)
