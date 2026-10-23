import os
from typing import List, Dict, Any
from openai import OpenAI
import numpy as np


def moderation_reason_embedding(moderation_reasons: List[str]) -> Dict[str, Any]:
    """
    Embed moderation rationales for case retrieval using OpenAI's embeddings API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    embeddings = []
    for reason in moderation_reasons:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=reason
        )
        embedding = response.data[0].embedding
        embeddings.append(embedding)

    embeddings_array = np.array(embeddings)

    if len(embeddings) > 1:
        mean_embedding = np.mean(embeddings_array, axis=0).tolist()
        similarity_matrix = np.dot(embeddings_array, embeddings_array.T)
    else:
        mean_embedding = embeddings[0] if embeddings else []
        similarity_matrix = np.array([[1.0]]) if embeddings else np.array([])

    return {
        "reasons": moderation_reasons,
        "embeddings": embeddings,
        "mean_embedding": mean_embedding,
        "similarity_matrix": similarity_matrix.tolist(),
        "embedding_model": "text-embedding-3-small",
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
    }
