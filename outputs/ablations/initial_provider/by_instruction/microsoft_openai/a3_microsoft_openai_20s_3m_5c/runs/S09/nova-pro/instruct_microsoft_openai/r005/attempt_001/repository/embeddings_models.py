from typing import List, Tuple

def normalize_embedding(embedding: List[float]) -> List[float]:
    norm_val = sum(val ** 2 for val in embedding) ** 0.5
    return [val / norm_val for val in embedding]

def prepare_request(texts: List[str]) -> Tuple[str, str]:
    return 'text-embedding-ada-002', texts