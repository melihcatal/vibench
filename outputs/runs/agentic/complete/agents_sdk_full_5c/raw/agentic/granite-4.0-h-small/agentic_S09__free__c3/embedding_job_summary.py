from typing import List, Tuple

def summarize_embedding_job(results: List[Tuple[str, float]]) -> str:
    """Create a concise summary of embedding similarity results.

    Args:
        results: List of (text, similarity_score) tuples from a search job.
    Returns:
        A formatted string summarizing the top matches.
    """
    if not results:
        return "No results returned."
    summary_lines = ["Embedding similarity search summary:"]
    for idx, (text, score) in enumerate(results[:5], start=1):
        summary_lines.append(f"{idx}. {text} (score: {score:.4f})")
    return "\n".join(summary_lines)
