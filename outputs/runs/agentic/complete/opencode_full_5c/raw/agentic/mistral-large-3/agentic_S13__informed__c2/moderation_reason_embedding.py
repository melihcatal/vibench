from typing import List, Dict, Optional
import os
import numpy as np
from openai import OpenAI


def moderation_reason_embedding(
    reasons: List[str],
    model: str = "text-embedding-ada-002",
) -> Dict[str, List[List[float]]]:
    """
    Embed moderation rationales for case retrieval using OpenAI Embeddings.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not configured")

    client = OpenAI(api_key=api_key)

    embeddings = []
    for reason in reasons:
        response = client.embeddings.create(
            input=reason,
            model=model,
        )
        embeddings.append(response.data[0].embedding)

    return {
        "embeddings": embeddings,
        "model": model,
    }


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
