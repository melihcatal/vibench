from scipy import spatial

def similarity_score(embedding1, embedding2):
    return 1 - spatial.distance.cosine(embedding1, embedding2)