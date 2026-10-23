# similarity_score.py
"""
["SAME-SCENARIO"] Compute cosine similarity between two embedding vectors.
"""

import math
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors.

    Args:
        vec1 (List[float]): First embedding vector.
        vec2 (List[float]): Second embedding vector.

    Returns:
        float: Cosine similarity score (0 to 1).
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must be the same length")
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) != 3:
        print("Usage: python similarity_score.py <vec1> <vec2>")
        sys.exit(1)
    vec1 = json.loads(sys.argv[1])
    vec2 = json.loads(sys.argv[2])
    score = cosine_similarity(vec1, vec2)
    print(f"Cosine similarity: {score:.4f}")
