from typing import List

def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    normalized = []
    for embedding in embeddings:
        norm_embedding = [float(i)/sum(embedding) for i in embedding]
        normalized.append(norm_embedding)
    return normalized