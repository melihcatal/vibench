import numpy as np

def cosine_similarity(embedding1, embedding2):
    embedding1_np = np.array(embedding1)
    embedding2_np = np.array(embedding2)
    dot_product = np.dot(embedding1_np, embedding2_np)
    norm_embedding1 = np.linalg.norm(embedding1_np)
    norm_embedding2 = np.linalg.norm(embedding2_np)
    similarity = dot_product / (norm_embedding1 * norm_embedding2)
    return similarity

def similarity_score(embedding1, embedding2):
    return {"similarity": cosine_similarity(embedding1, embedding2)}
