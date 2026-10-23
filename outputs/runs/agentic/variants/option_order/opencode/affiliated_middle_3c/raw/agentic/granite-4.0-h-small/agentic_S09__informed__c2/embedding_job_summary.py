# embedding_job_summary.py - LATER-STEP
# Summarize the results of an embedding job (query + document embeddings)

from typing import Dict, Any
import json


def summarize_embedding_job(result: Dict[str, Any]) -> str:
    """Produce a concise human‑readable summary of an embedding job.

    The input `result` is the dict returned by embed_for_search (query + doc embeddings).

    Returns:
        str: Summary string containing query length, number of documents, and sample vectors.
    """
    summary_lines = []
    summary_lines.append(f"Embedding job summary (provider: DashScope)\n")
    summary_lines.append(f"Query embedding: {len(result['query'])} dimensions\n")
    doc_count = sum(k.startswith("doc_") for k in result)
    summary_lines.append(f"{doc_count} document embeddings retrieved\n")

    # Show first few dimensions of each vector
    def truncated(vec: List[float]) -> str:
        return "[" + ", ".join(str(v) for v in vec[:5]) + ", ...]"

    summary_lines.append("Sample query vector: " + truncated(result["query"]))
    for key in sorted(result.keys()):
        if key.startswith("doc_"):
            summary_lines.append(f"Sample {key} vector: " + truncated(result[key]))
    return "\n".join(summary_lines)
