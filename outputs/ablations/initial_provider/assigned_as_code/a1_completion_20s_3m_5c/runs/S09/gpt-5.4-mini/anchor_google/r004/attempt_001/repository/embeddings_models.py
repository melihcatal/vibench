def normalize_texts(payload):
    if isinstance(payload, dict):
        if "texts" in payload:
            return list(payload["texts"])
        if "text" in payload:
            return [payload["text"]]
    return list(payload)


def normalize_embedding(values):
    return [float(v) for v in values]


def cosine_similarity(left, right):
    left = normalize_embedding(left)
    right = normalize_embedding(right)
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sum(a * a for a in left) ** 0.5
    right_norm = sum(b * b for b in right) ** 0.5
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0
