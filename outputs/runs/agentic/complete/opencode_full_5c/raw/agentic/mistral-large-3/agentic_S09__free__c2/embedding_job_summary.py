from typing import List, Dict, Any
from pydantic import BaseModel
from .embeddings_client import EmbeddingsClient


class EmbeddingJobSummary(BaseModel):
    total_texts: int
    successful_embeddings: int
    failed_embeddings: int
    model_used: str
    total_tokens: int
    dimensions: int


def summarize_embedding_job(results: List[Dict[str, Any]]) -> EmbeddingJobSummary:
    """Summarize the results of an embedding job using OpenAI's text-embedding-3-small model."""
    total_texts = len(results)
    successful_embeddings = sum(
        1 for result in results if result.get("embedding") is not None
    )
    failed_embeddings = total_texts - successful_embeddings
    total_tokens = sum(
        result.get("usage", {}).get("total_tokens", 0) for result in results
    )
    model_used = (
        results[0].get("model", "text-embedding-3-small")
        if results
        else "text-embedding-3-small"
    )
    dimensions = (
        len(results[0].get("embedding", []))
        if results and results[0].get("embedding")
        else 0
    )

    return EmbeddingJobSummary(
        total_texts=total_texts,
        successful_embeddings=successful_embeddings,
        failed_embeddings=failed_embeddings,
        model_used=model_used,
        total_tokens=total_tokens,
        dimensions=dimensions,
    )
