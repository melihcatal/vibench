def normalize_texts(payload):
    if isinstance(payload, dict):
        if "texts" in payload:
            texts = payload["texts"]
            return list(texts) if isinstance(texts, (list, tuple)) else [texts]
        if "text" in payload:
            return [payload["text"]]
    if isinstance(payload, (list, tuple)):
        return list(payload)
    return [payload]


def embedding_vector(response):
    return list(response.embeddings[0].values)


def embedding_vectors(response):
    return [list(item.values) for item in response.embeddings]


def cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sum(a * a for a in left) ** 0.5
    right_norm = sum(b * b for b in right) ** 0.5
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)
