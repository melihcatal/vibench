import numpy as np
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    # These would typically come from an embedding service
    embedding1 = [0.1, 0.2, 0.3, 0.4, 0.5]
    embedding2 = [0.1, 0.2, 0.3, 0.4, 0.5]  # Identical
    embedding3 = [0.5, 0.4, 0.3, 0.2, 0.1]  # Different

    score12 = cosine_similarity(embedding1, embedding2)
    score13 = cosine_similarity(embedding1, embedding3)

    print(f"Similarity between embedding1 and embedding2 (identical): {score12}")
    print(f"Similarity between embedding1 and embedding3 (different): {score13}")
