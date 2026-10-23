from numpy import dot
from numpy.linalg import norm

def cosine_similarity(vecA: list, vecB: list) -> float:
  return dot(vecA, vecB) / (norm(vecA) * norm(vecB))