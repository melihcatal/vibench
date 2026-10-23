def normalize_text_payload(payload):
    if isinstance(payload, dict):
        if 'text' in payload:
            return payload['text']
        if 'texts' in payload:
            return payload['texts']
    return payload


def extract_embedding_vector(response):
    return response.data[0].embedding


def extract_embeddings_vectors(response):
    return [item.embedding for item in response.data]
