from typing import List

def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    normalized = []
    for embedding in embeddings:
        normalized.append([float(f) for f in embedding])
    return normalized