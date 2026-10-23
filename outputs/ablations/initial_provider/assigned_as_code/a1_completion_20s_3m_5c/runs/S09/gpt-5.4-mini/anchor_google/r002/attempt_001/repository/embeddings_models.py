def normalize_texts(payload):
    if isinstance(payload, dict):
        if "texts" in payload:
            return list(payload["texts"])
        if "text" in payload:
            return [payload["text"]]
    return list(payload)


def extract_embedding(response):
    return list(response.embeddings[0].values)


def extract_embeddings(response):
    return [list(item.values) for item in response.embeddings]


def cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sum(a * a for a in left) ** 0.5
    right_norm = sum(b * b for b in right) ** 0.5
    return dot / (left_norm * right_norm)
