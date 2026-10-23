import json

import boto3

from.embeddings_client import get_bedrock_client
from.embeddings_models import normalize_payload, parse_response


def similarity_score(payload1, payload2, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    embedding1 = embed_text(payload1, config)
    embedding2 = embed_text(payload2, config)
    cosine_similarity = calculate_cosine_similarity(embedding1, embedding2)
    return {"similarity_score": cosine_similarity}


def calculate_cosine_similarity(embedding1, embedding2):
    import numpy as np
    embedding1 = np.array(embedding1["embedding"])
    embedding2 = np.array(embedding2["embedding"])
    dot_product = np.dot(embedding1, embedding2)
    norm_embedding1 = np.linalg.norm(embedding1)
    norm_embedding2 = np.linalg.norm(embedding2)
    cosine_similarity = dot_product / (norm_embedding1 * norm_embedding2)
    return cosine_similarity