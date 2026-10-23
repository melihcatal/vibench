def normalize_embedding_response(response):
    if isinstance(response, dict) and 'data' in response:
        return response['data'][0]['embedding']
    return response.data[0].embedding


def normalize_texts(payload):
    texts = payload.get('texts')
    if texts is not None:
        return texts
    return [payload['text']]


def cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sum(a * a for a in left) ** 0.5
    right_norm = sum(b * b for b in right) ** 0.5
    return dot / (left_norm * right_norm)
