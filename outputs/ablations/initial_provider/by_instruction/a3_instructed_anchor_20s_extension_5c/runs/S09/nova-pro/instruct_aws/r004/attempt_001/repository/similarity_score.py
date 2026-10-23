from scipy import spatial

def similarity_score(embedding1: list, embedding2: list) -> float:
    return 1 - spatial.distance.cosine(embedding1, embedding2)