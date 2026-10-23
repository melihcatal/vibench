from numpy import dot
from numpy.linalg import norm


def similarity_score(vec1: list, vec2: list) -> float:
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))
