import os
from typing import List, Dict, Any
import numpy as np


def moderation_reason_embedding(reasons: List[str]) -> Dict[str, Any]:
    """
    Embed moderation rationales for case retrieval using OpenAI Embeddings.
    """
    import openai

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    try:
        # Combine reasons for embedding
        combined_text = " ".join(reasons)

        response = client.embeddings.create(
            model="text-embedding-3-small", input=combined_text, encoding_format="float"
        )

        embedding = response.data[0].embedding

        # Convert to numpy array for easier manipulation
        embedding_array = np.array(embedding)

        return {
            "reasons": reasons,
            "embedding": embedding,
            "embedding_dim": len(embedding),
            "provider": "openai",
            "model": "text-embedding-3-small",
            "norm": float(np.linalg.norm(embedding_array)),
        }

    except Exception as e:
        return {
            "reasons": reasons,
            "embedding": [],
            "error": str(e),
            "provider": "openai",
        }


def similarity_search(
    query_embedding: List[float], case_embeddings: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Find similar moderation cases using cosine similarity.
    """
    import numpy as np

    query_vec = np.array(query_embedding)
    query_norm = np.linalg.norm(query_vec)

    similarities = []

    for case in case_embeddings:
        case_vec = np.array(case.get("embedding", []))
        if len(case_vec) == len(query_vec):
            case_norm = np.linalg.norm(case_vec)
            if query_norm > 0 and case_norm > 0:
                similarity = np.dot(query_vec, case_vec) / (query_norm * case_norm)
                similarities.append(
                    {
                        "case_id": case.get("case_id", ""),
                        "similarity": float(similarity),
                        "reasons": case.get("reasons", []),
                    }
                )

    # Sort by similarity descending
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]
