from typing import List, Dict

def normalize_embedding(embedding: Dict[str, float]) -> List[float]:
    return list(embedding.values())