import numpy as np

MODEL_NAME = 'embed-english-v3.0'

def normalize_embedding(embedding: list[float]) -&gt; np.ndarray:
    emb_array = np.array(embedding)
    norm = np.linalg.norm(emb_array)
    if norm == 0:
        return emb_array
    return emb_array / norm

def cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -&gt; float:
    return np.dot(emb1, emb2)