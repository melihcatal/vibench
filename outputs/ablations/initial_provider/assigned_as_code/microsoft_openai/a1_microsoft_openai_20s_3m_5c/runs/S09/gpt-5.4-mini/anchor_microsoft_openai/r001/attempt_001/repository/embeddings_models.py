def normalize_texts(texts):
    if texts is None:
        return []
    if isinstance(texts, str):
        return [texts]
    return list(texts)


def normalize_embedding_response(response):
    data = []
    for item in response.data:
        data.append(item.embedding)
    return {'embeddings': data}


def cosine_similarity(vector_a, vector_b):
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = sum(a * a for a in vector_a) ** 0.5
    norm_b = sum(b * b for b in vector_b) ** 0.5
    return dot / (norm_a * norm_b)
