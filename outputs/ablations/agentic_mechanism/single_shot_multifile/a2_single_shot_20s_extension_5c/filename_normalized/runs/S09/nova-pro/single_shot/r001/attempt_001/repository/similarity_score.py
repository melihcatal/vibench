from embeddings_client import EmbeddingsClient
import numpy as np

client = EmbeddingsClient()

def similarity_score(embedding1, embedding2):
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    cosine_similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return cosine_similarity