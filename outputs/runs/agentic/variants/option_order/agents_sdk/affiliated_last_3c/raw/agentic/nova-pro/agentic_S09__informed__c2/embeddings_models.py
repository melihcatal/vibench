from typing import List

def normalize_embedding(embedding: List[float]) -> List[float]:
    norm = sum([e**2 for e in embedding])**0.5
    return [e / norm for e in embedding]