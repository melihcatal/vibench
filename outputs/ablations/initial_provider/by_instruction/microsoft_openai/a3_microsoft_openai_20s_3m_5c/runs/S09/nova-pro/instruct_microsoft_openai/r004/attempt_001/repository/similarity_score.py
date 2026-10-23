from scipy.spatial.distance import cosine

def similarity_score(embedding1: List[float], embedding2: List[float]):
    return 1 - cosine(embedding1, embedding2)