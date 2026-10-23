def normalize_texts(payload):
    if isinstance(payload, dict):
        if 'texts' in payload:
            return list(payload['texts'])
        if 'text' in payload:
            return [payload['text']]
    if isinstance(payload, str):
        return [payload]
    return list(payload)


def embedding_vector_from_response(response):
    return response.data[0].embedding


def embedding_vectors_from_response(response):
    return [item.embedding for item in response.data]
