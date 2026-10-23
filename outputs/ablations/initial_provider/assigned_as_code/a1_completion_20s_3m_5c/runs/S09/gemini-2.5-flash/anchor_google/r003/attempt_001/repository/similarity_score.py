import numpy as np
from typing import List, Dict, Any

def similarity_score(payload: Dict[str, Any]) -> Dict[str, float]:
    """Computes the cosine similarity between two embedding vectors."""
    embedding1 = payload.get("embedding1")
    embedding2 = payload.get("embedding2")

    if not embedding1 or not embedding2:
        raise ValueError("Payload must contain 'embedding1' and 'embedding2' lists.")

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # Compute cosine similarity
    # cosine_similarity = (A . B) / (||A|| * ||B||)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return {"similarity_score": 0.0} # Or handle as an error, depending on desired behavior

    score = dot_product / (norm_vec1 * norm_vec2)
    return {"similarity_score": float(score)}
