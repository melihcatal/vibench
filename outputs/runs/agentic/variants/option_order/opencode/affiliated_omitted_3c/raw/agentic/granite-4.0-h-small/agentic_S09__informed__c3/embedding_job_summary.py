import os
import json
from typing import List

# Provider identified by SDK import and model identifier


class EmbeddingJobSummary:
    """Summarizes embedding job results from the Direct Embeddings API."""

    @staticmethod
    def summarize(results: List[float]) -> str:
        """Returns a concise summary string of embedding job outputs."""
        n = len(results)
        avg = sum(results) / n if n else 0.0
        return f"Embedded {n} items with average similarity score {avg:.4f}"

    @classmethod
    def detailed_summary(cls, embeddings: List[List[float]]) -> str:
        """Returns detailed summary including count and shape info."""
        rows = len(embeddings)
        dims = len(embeddings[0]) if rows else 0
        return (
            f"Embedding job produced {rows} vectors, each of dimension {dims}.\n"
            f"Sample first vector: {embeddings[0] if rows else '[]'}"
        )
