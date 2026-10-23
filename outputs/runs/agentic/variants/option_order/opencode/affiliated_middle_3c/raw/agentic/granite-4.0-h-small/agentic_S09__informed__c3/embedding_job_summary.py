import os
from embedding_job_results import EmbeddingJobResult  # placeholder import


def summarize_embedding_job(results: list[EmbeddingJobResult]) -> str:
    """Generate a concise summary of an embedding job.

    Summarizes count of successful embeddings, failures, and overall latency.
    """
    if not results:
        return "No embedding results to summarize."
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful
    total_latency = sum(r.latency_ms for r in results)
    avg_latency = total_latency / len(results)
    summary = (
        f"Embedding job summary -> Total: {len(results)}, "
        f"Successful: {successful}, Failed: {failed}. "
        f"Average latency: {avg_latency:.2f} ms."
    )
    return summary
