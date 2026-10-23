import numpy as np
from scipy.spatial.distance import cosine
from typing import List, Dict

def similarity_score(payload: Dict) -> Dict:
    embedding1 = payload.get("embedding1")
    embedding2 = payload.get("embedding2")

    if not isinstance(embedding1, list) or not isinstance(embedding2, list):
        raise ValueError("Payload must contain 'embedding1' and 'embedding2' as lists of numbers.")

    if not embedding1 or not embedding2:
        raise ValueError("Embeddings cannot be empty.")

    # Convert lists to numpy arrays
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    if vec1.shape != vec2.shape:
        raise ValueError("Embeddings must have the same dimensions.")

    # Compute cosine similarity. Note: scipy.spatial.distance.cosine returns distance, so 1 - distance is similarity.
    # Handle cases where vectors are zero to avoid NaN. Cosine similarity of zero vectors is undefined, 
    # but often treated as 0 or 1 depending on context. Here, if either is zero vector, similarity is 0.
    if np.all(vec1 == 0) or np.all(vec2 == 0):
        similarity = 0.0
    else:
        similarity = 1 - cosine(vec1, vec2)
    
    return {"similarity": float(similarity)}
