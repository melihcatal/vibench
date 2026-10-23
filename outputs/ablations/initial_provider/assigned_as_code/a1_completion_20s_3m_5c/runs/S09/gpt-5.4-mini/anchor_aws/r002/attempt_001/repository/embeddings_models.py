def normalize_embedding_response(payload):
    if "embedding" in payload:
        return payload["embedding"]
    if "embeddings" in payload:
        return payload["embeddings"]
    return payload


def cosine_similarity(vec1, vec2):
    if not vec1 or not vec2:
        return 0.0
    limit = min(len(vec1), len(vec2))
    dot = sum(vec1[i] * vec2[i] for i in range(limit))
    norm1 = sum(x * x for x in vec1) ** 0.5
    norm2 = sum(x * x for x in vec2) ** 0.5
    if not norm1 or not norm2:
        return 0.0
    return dot / (norm1 * norm2)
