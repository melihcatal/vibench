import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def similarity_score(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.",
    """"""
    return float(cosine_similarity([vec1], [vec2])[0][0])