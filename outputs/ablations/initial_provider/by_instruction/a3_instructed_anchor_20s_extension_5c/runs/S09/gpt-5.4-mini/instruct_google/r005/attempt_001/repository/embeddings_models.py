import math


def vector_from_response(response):
    if hasattr(response, "embeddings") and response.embeddings:
        first = response.embeddings[0]
        if hasattr(first, "values"):
            return list(first.values)
        if isinstance(first, dict) and "values" in first:
            return list(first["values"])
    if hasattr(response, "embedding") and response.embedding is not None:
        embedding = response.embedding
        return list(getattr(embedding, "values", embedding))
    if isinstance(response, dict):
        if "embeddings" in response and response["embeddings"]:
            first = response["embeddings"][0]
            return list(first.get("values", first))
        if "embedding" in response:
            embedding = response["embedding"]
            return list(embedding.get("values", embedding))
    return []


def normalize_vector(vector):
    norm = math.sqrt(sum(value * value for value in vector))
    if not norm:
        return [0.0 for _ in vector]
    return [value / norm for value in vector]


def cosine_similarity(left, right):
    if len(left) != len(right):
        raise ValueError("vector length mismatch")
    left_n = normalize_vector(left)
    right_n = normalize_vector(right)
    return sum(a * b for a, b in zip(left_n, right_n))
