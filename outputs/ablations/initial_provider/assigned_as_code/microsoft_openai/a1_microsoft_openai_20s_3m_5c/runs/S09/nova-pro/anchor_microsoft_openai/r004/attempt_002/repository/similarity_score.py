import numpy as np

from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def similarity_score(embedding1, embedding2):
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


def compute_similarity(payload, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response1 = client.embeddings.create(model='text-embedding-3-small', input=payload['text1'])
    response2 = client.embeddings.create(model='text-embedding-3-small', input=payload['text2'])
    embedding1 = normalize_embedding_response(response1.data[0])
    embedding2 = normalize_embedding_response(response2.data[0])
    return {'similarity_score': similarity_score(embedding1, embedding2)}