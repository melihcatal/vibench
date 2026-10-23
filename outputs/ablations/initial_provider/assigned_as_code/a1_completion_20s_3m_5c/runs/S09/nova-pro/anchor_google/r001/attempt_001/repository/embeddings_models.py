import numpy as np


def normalize_embedding_response(response):
    return list(response.embeddings[0].values())


def normalize_embedding_request(payload):
    return {"text": payload["text"]}