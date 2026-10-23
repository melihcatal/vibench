def extract_embedding(response):
    return list(response.embeddings[0].values)


def extract_embeddings(response):
    return [list(item.values) for item in response.embeddings]


def cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sum(a * a for a in left) ** 0.5
    right_norm = sum(b * b for b in right) ** 0.5
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def normalize_texts(payload):
    texts = payload.get("texts")
    if texts is None:
        return [payload["text"]]
    return list(texts)
