def normalize_embedding_response(response):
    if isinstance(response, dict) and "embedding" in response:
        return {"embedding": response["embedding"]}
    if isinstance(response, dict) and "embeddings" in response:
        return {"embeddings": response["embeddings"]}
    return response


def cosine_similarity(left, right):
    if not left or not right:
        return 0.0
    length = min(len(left), len(right))
    dot = sum(left[i] * right[i] for i in range(length))
    left_norm = sum(x * x for x in left) ** 0.5
    right_norm = sum(x * x for x in right) ** 0.5
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def embed_payload(texts):
    if isinstance(texts, str):
        return {"inputText": texts}
    return {"inputTextList": list(texts)}
