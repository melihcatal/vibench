import math


def normalize_embedding(embedding):
    magnitude = math.sqrt(sum(value * value for value in embedding))
    if not magnitude:
        return embedding
    return [value / magnitude for value in embedding]


def cosine_similarity(left, right):
    left_norm = normalize_embedding(left)
    right_norm = normalize_embedding(right)
    return sum(a * b for a, b in zip(left_norm, right_norm))


def parse_embedding_response(response):
    return [item.embedding for item in response.data]
