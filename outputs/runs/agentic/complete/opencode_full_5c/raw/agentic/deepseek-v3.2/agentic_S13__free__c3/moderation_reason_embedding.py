import os
from openai import OpenAI
from typing import List, Dict, Any
import numpy as np


def moderation_reason_embedding(moderation_reason: str) -> Dict[str, Any]:
    """
    Embed moderation rationales for case retrieval using OpenAI's embeddings API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model="text-embedding-3-small", input=moderation_reason, encoding_format="float"
    )

    embedding = response.data[0].embedding

    return {
        "reason": moderation_reason,
        "embedding": embedding,
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": len(embedding),
        "provider": "OpenAI",
    }


def batch_moderation_reason_embedding(reasons: List[str]) -> List[Dict[str, Any]]:
    """
    Embed multiple moderation rationales for case retrieval.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model="text-embedding-3-small", input=reasons, encoding_format="float"
    )

    results = []
    for i, data in enumerate(response.data):
        results.append(
            {
                "reason": reasons[i],
                "embedding": data.embedding,
                "embedding_model": "text-embedding-3-small",
                "embedding_dimensions": len(data.embedding),
                "provider": "OpenAI",
            }
        )

    return results


def similarity_search(
    query_embedding: List[float],
    reason_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Find similar moderation reasons using cosine similarity.
    """
    query_vec = np.array(query_embedding)

    similarities = []
    for reason_data in reason_embeddings:
        reason_vec = np.array(reason_data["embedding"])

        # Cosine similarity
        dot_product = np.dot(query_vec, reason_vec)
        norm_query = np.linalg.norm(query_vec)
        norm_reason = np.linalg.norm(reason_vec)

        if norm_query == 0 or norm_reason == 0:
            similarity = 0
        else:
            similarity = dot_product / (norm_query * norm_reason)

        similarities.append(
            {
                "reason": reason_data["reason"],
                "similarity": float(similarity),
                "original_data": reason_data,
            }
        )

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]
