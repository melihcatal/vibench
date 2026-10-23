from typing import List, Tuple


def normalize_embedding(embedding: List[float]) -> List[float]:
    norm_embedding = [float(i) for i in embedding]
    return norm_embedding


def parse_response(response: dict) -> Tuple[List[float], ...]:
    data = response["data"][0]
    embedding = data["embedding"]
    return normalize_embedding(embedding), ...
