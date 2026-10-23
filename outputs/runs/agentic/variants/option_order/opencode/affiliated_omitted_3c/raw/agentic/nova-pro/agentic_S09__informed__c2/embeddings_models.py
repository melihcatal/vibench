from typing import List, Tuple


def normalize_embedding(embedding: List[float]) -> List[float]:
    norm_val = sum(e**2 for e in embedding) ** 0.5
    return [e / norm_val for e in embedding]


def embed_request(text: str) -> dict:
    return {"model": "text-embedding-v1", "input": text}


def embed_response(response: dict) -> List[float]:
    return response["output"]["embedding"]
