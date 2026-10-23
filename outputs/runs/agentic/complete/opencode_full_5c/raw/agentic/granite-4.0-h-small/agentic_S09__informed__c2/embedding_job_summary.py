import json


def embedding_job_summary(job_results: dict):
    """Summarize embedding job results.

    Expects a dictionary with keys like 'query_embedding' and 'doc_embeddings'.
    Returns a concise human-readable summary.
    """
    summary_lines = []
    summary_lines.append("=== Embedding Job Summary ===")
    summary_lines.append(
        f"Query Embedding: {json.dumps(job_results.get('query_embedding', []))}"
    )
    doc_embs = job_results.get("doc_embeddings", [])
    summary_lines.append(f"Document Embeddings Count: {len(doc_embs)}")
    # Show first 3 embeddings for brevity
    first_three = doc_embs[:3]
    summary_lines.append("First few document embeddings:")
    for i, emb in enumerate(first_three, start=1):
        summary_lines.append(f"  {i}: {emb}")
    return "\n".join(summary_lines)
