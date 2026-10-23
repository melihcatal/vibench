import json
import math


def normalize_texts(texts):
    if isinstance(texts, str):
        return [texts]
    return [str(t) for t in texts]


def parse_bedrock_embedding_response(payload):
    data = json.loads(payload.decode("utf-8") if isinstance(payload, (bytes, bytearray)) else payload)
    if "embedding" in data:
        return data["embedding"]
    if "embeddings" in data:
        return data["embeddings"]
    return data


def cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)
