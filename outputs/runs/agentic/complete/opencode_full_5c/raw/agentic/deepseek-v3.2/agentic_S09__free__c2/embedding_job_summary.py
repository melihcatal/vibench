import os
from typing import List, Dict, Any
from openai import OpenAI
import json
from datetime import datetime


def embedding_job_summary(
    texts: List[str], model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Summarize embedding job results using OpenAI's embeddings API.

    Args:
        texts: List of text strings that were embedded
        model: The OpenAI embedding model used

    Returns:
        Dict containing job summary statistics
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Generate embeddings
    response = client.embeddings.create(
        model=model, input=texts, encoding_format="float"
    )

    embeddings = [item.embedding for item in response.data]

    # Calculate statistics
    total_texts = len(texts)
    total_tokens = sum(item.usage.total_tokens for item in response.data)

    # Calculate average text length
    avg_text_length = (
        sum(len(text) for text in texts) / total_texts if total_texts > 0 else 0
    )

    # Calculate embedding dimensions
    embedding_dimensions = len(embeddings[0]) if embeddings else 0

    # Calculate average embedding norm
    import numpy as np

    norms = [np.linalg.norm(np.array(emb)) for emb in embeddings]
    avg_norm = np.mean(norms) if norms else 0

    # Create summary
    summary = {
        "job_timestamp": datetime.now().isoformat(),
        "provider": "OpenAI",
        "model": model,
        "total_texts": total_texts,
        "total_tokens": total_tokens,
        "avg_text_length": round(avg_text_length, 2),
        "embedding_dimensions": embedding_dimensions,
        "avg_embedding_norm": round(avg_norm, 4),
        "cost_estimate_usd": round(
            total_tokens * 0.0000001, 6
        ),  # OpenAI embedding pricing
        "success_rate": 1.0,  # All embeddings generated successfully
        "embeddings_generated": len(embeddings),
    }

    return summary
