# [LATER-STEP] incident_summary.py
"""Summarize error-log findings for incident review."""

from __future__ import annotations
from collections import Counter
from observability_models import LogResponse, LogEmbeddingResult


def summarize_incident(logs: LogResponse, embeddings: LogEmbeddingResult) -> dict:
    """Produce a concise incident summary from error logs and their embeddings.

    Args:
        logs (LogResponse): Normalized error log events.
        embeddings (LogEmbeddingResult): Embedding vectors for the same messages.

    Returns:
        dict: A summary containing count, top messages, and semantic similarity flags.
    """
    # Count occurrences
    counts = Counter(
        log["severity"]
        for log in logs.as_list()
        if log.get("severity") in ("error", "critical")
    )
    severity_breakdown = dict(counts)

    # Simple keyword extraction from messages (placeholder for later NLP)
    top_messages = [log["message"] for log in logs.as_list()][:5]

    # Embedding similarity flag (placeholder)
    similar = len(embeddings.embeddings) > 0

    return {
        "summary": "Error log incident summary",
        "severity_count": severity_breakdown,
        "top_messages": top_messages,
        "similar_embeddings": similar,
    }
