import json
import math


def normalize_texts(payload):
    if payload is None:
        return []
    if isinstance(payload, dict):
        if "texts" in payload:
            return [str(text) for text in payload["texts"]]
        if "text" in payload:
            return [str(payload["text"])]
    return [str(item) for item in payload]


def normalize_query_and_documents(payload):
    query = str(payload["query"])
    documents = [str(item) for item in payload["documents"]]
    return query, documents


def parse_embedding_response(body):
    if isinstance(body, (bytes, bytearray)):
        body = body.decode("utf-8")
    if isinstance(body, str):
        data = json.loads(body)
    else:
        data = body
    embedding = data.get("embedding") or data.get("embeddings", [None])[0]
    return {"embedding": embedding}


def cosine_similarity(left, right):
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)
