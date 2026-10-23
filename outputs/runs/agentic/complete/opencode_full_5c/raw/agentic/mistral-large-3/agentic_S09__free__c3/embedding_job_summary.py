from typing import List, Dict, Any
import numpy as np
from datetime import datetime


def summarize_embedding_job(
    job_id: str,
    texts: List[str],
    embeddings: List[List[float]],
    model: str = "text-embedding-3-small",
) -> Dict[str, Any]:
    """
    Summarizes the results of an embedding job using OpenAI's embeddings.

    Args:
        job_id: Unique identifier for the embedding job.
        texts: List of input texts that were embedded.
        embeddings: List of embedding vectors corresponding to the input texts.
        model: OpenAI embedding model used. Defaults to "text-embedding-3-small".

    Returns:
        Dict[str, Any]: Summary of the embedding job results.
    """
    embedding_dim = len(embeddings[0]) if embeddings else 0
    avg_embedding = np.mean(embeddings, axis=0).tolist() if embeddings else []

    summary = {
        "job_id": job_id,
        "timestamp": datetime.utcnow().isoformat(),
        "model_used": model,
        "total_texts_processed": len(texts),
        "embedding_dimension": embedding_dim,
        "average_embedding": avg_embedding,
        "texts_sample": texts[:5],  # Sample of first 5 texts
        "statistics": {
            "embedding_mean": np.mean(avg_embedding),
            "embedding_std": np.std(avg_embedding),
        },
    }

    return summary
