# embedding_job_summary.py
import os
from typing import List, Tuple
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import check_response

def summarize_embedding_job(results: List[Tuple[str, float]]) -> str:
    """Produce a concise text summary of an embedding similarity job.

    Args:
        results (List[Tuple[str, float]]): ranked document-similarity pairs.

    Returns:
        str: multi-line summary string.
    """
    if not results:
        return "No results were returned."
    lines = [f"Found {len(results)} matches:"]
    for i, (doc, score) in enumerate(results, start=1):
        lines.append(f"  {i}. {doc[:80]}{'...' if len(doc) > 80 else ''} (score: {score:.3f})")
    return "\\n".join(lines)
