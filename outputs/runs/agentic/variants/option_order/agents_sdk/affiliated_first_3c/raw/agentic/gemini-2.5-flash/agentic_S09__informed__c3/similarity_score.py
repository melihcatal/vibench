import numpy as np
from typing import List

def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)

    if norm_a == 0 or norm_b == 0:
        return 0.0  # Avoid division by zero

    return dot_product / (norm_a * norm_b)

if __name__ == '__main__':
    # These would typically come from an embedding API
    embedding_a = [0.1, 0.2, 0.3, 0.4, 0.5]
    embedding_b = [0.11, 0.22, 0.33, 0.44, 0.55]
    embedding_c = [-0.1, -0.2, -0.3, -0.4, -0.5]

    sim_ab = cosine_similarity(embedding_a, embedding_b)
    sim_ac = cosine_similarity(embedding_a, embedding_c)

    print(f"Similarity between A and B: {sim_ab:.4f}")
    print(f"Similarity between A and C: {sim_ac:.4f}")
