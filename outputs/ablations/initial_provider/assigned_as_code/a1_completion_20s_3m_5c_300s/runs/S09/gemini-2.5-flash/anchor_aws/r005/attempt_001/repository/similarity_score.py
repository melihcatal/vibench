import numpy as np

def cosine_similarity(embedding1, embedding2):
    embedding1_np = np.array(embedding1)
    embedding2_np = np.array(embedding2)
    
    dot_product = np.dot(embedding1_np, embedding2_np)
    norm_a = np.linalg.norm(embedding1_np)
    norm_b = np.linalg.norm(embedding2_np)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)

def similarity_score(embedding_pair):
    embedding1 = embedding_pair["embedding1"]
    embedding2 = embedding_pair["embedding2"]
    return {"similarity": cosine_similarity(embedding1, embedding2)}
