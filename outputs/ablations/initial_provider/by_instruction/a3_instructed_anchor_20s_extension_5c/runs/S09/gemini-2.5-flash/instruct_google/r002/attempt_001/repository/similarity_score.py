import numpy as np

def similarity_score(embedding1: list[float], embedding2: list[float]) -> float:
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
