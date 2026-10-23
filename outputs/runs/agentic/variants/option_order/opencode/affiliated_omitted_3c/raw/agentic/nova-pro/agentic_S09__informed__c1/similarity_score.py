from numpy import dot
from numpy.linalg import norm


def cosine_similarity(embedding1: list, embedding2: list) -> float:
    return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
