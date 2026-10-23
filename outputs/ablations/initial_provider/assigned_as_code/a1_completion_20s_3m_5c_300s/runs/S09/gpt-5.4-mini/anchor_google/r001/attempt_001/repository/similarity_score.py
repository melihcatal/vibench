import math

from embed_text import embed_text


def similarity_score(payload, config=None):
    left = embed_text({"text": payload["text_a"]}, config=config)["embedding"]
    right = embed_text({"text": payload["text_b"]}, config=config)["embedding"]
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    return {"score": dot / (left_norm * right_norm) if left_norm and right_norm else 0.0}
