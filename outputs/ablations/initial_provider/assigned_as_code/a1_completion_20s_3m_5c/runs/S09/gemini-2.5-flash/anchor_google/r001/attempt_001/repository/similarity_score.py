import numpy as np
from typing import List
from embeddings_models import SimilarityScoreRequest

def similarity_score(payload: dict) -> dict:
    embedding1 = payload.get("embedding1")
    embedding2 = payload.get("embedding2")

    if not embedding1 or not embedding2:
        raise ValueError("Payload must contain 'embedding1' and 'embedding2'.")
    
    # Ensure embeddings are numpy arrays for calculation
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    if vec1.shape != vec2.shape:
        raise ValueError("Embedding vectors must have the same dimension.")

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return {"similarity_score": 0.0} # Or raise an error, depending on desired behavior for zero vectors

    score = dot_product / (norm_vec1 * norm_vec2)
    
    return {"similarity_score": float(score)}
