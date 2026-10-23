import numpy as np

from embeddings_client import get_bedrock_client


def similarity_score(embedding1, embedding2):
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    cosine_similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return {"similarity_score": cosine_similarity}