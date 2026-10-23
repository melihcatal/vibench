import math


def normalize_text(value):
    return "" if value is None else str(value).strip()


def normalize_texts(values):
    return [normalize_text(value) for value in values]


def cosine_similarity(left, right):
    if not left or not right:
        return 0.0
    size = min(len(left), len(right))
    dot = sum(left[i] * right[i] for i in range(size))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def make_embedding_response(embedding):
    return {"embedding": embedding}
