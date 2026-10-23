import numpy as np
from typing import List, Dict, Any

def similarity_score(payload: Dict[str, Any]) -> Dict[str, float]:
    embedding1 = np.array(payload["embedding1"])
    embedding2 = np.array(payload["embedding2"])

    dot_product = np.dot(embedding1, embedding2)
    norm_a = np.linalg.norm(embedding1)
    norm_b = np.linalg.norm(embedding2)

    if norm_a == 0 or norm_b == 0:
        return {"similarity": 0.0}

    cosine_similarity = dot_product / (norm_a * norm_b)
    return {"similarity": float(cosine_similarity)}
