import json
from typing import List, Dict


def summarize_embedding_job(results: List[Dict[str, float]]) -> str:
    """Summarize embedding job results with basic statistics.

    Args:
        results (List[Dict[str, float]]): List of document index and similarity scores.

    Returns:
        str: Human‑readable summary including count, min, max, avg similarity.
    """
    if not results:
        return "No embeddings computed."
    scores = [score for _, score in results.items()]
    count = len(scores)
    avg = sum(scores) / count
    mini = min(scores)
    maxi = max(scores)
    return f"Embedding job summary:\n  Documents processed: {count}\n  Minimum similarity: {mini:.4f}\n  Maximum similarity: {maxi:.4f}\n  Average similarity: {avg:.4f}"
