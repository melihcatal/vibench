import numpy as np
from typing import List

def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    a = np.asarray(emb1)
    b = np.asarray(emb2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def search_similarities(query_emb: List[float], doc_embs: List[List[float]]) -> List[float]:
    return [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embs]