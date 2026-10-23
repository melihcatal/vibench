def create_embed_request(texts, task_type=None, title=None):
    if isinstance(texts, str):
        contents = [texts]
    else:
        contents = texts
    request = {"contents": contents}
    if task_type:
        request["task_type"] = task_type
    if title:
        request["title"] = title
    return request

def parse_embed_response(response):
    return [list(embedding.values) for embedding in response.embeddings]

def normalize_embedding(embedding_vector):
    # Gemini embeddings are typically already normalized, but this is a placeholder for custom normalization if needed.
    # For L2 normalization: np.linalg.norm(embedding_vector)
    return embedding_vector
