import json
from typing import Any


def summarize_embedding_job(results: list[Any]) -> str:
    """Summarize embedding job results (e.g., latency, count)."""
    if not results:
        return "No embedding results to summarize."
    # Assuming each result has a 'latency' field
    latencies = [r.get("latency", 0) for r in results]
    avg_latency = sum(latencies) / len(latencies)
    return f"Embedded {len(results)} items with average latency {avg_latency:.2f}ms."
