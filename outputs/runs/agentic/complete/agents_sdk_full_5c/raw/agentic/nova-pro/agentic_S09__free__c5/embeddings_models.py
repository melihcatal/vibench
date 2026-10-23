from typing import List

def normalize_embeddings(embeddings: List[float]) -> List[float]:
    norm = sum(e**2 for e in embeddings)**0.5
    return [e / norm for e in embeddings]
