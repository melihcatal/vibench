import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def similarity_score(text1, text2):
    from embed_text import embed_text
    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)
    return cosine_similarity(embedding1, embedding2)