from numpy import dot
from numpy.linalg import norm


def similarity_score(embedding1, embedding2):
    return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
