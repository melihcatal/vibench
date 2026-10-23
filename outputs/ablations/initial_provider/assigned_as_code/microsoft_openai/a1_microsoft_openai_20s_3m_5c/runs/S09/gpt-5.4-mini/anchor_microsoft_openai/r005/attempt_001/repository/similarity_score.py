import math

from embed_text import embed_text


def cosine_similarity(payload, config=None):
    config = config or {}
    left = embed_text({'text': payload['text_a']}, config)['embedding']
    right = embed_text({'text': payload['text_b']}, config)['embedding']
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    return {'similarity': dot / (left_norm * right_norm)}
