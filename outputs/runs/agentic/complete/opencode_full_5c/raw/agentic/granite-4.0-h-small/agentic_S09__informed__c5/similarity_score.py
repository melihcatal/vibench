# [SAME-SCENARIO] similarity_score.py
# Computes cosine similarity between two embedded texts

# Provider: OpenAI Embeddings (used via same client above)
# Integration signal: OPENAI_API_KEY environment variable

import math
from typing import List


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Cosine similarity between two embedding vectors.
    Returns a float between -1 and 1.
    """
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
