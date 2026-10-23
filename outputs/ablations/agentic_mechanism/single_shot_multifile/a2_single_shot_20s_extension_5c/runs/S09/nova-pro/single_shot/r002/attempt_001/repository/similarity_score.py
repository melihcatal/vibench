import numpy as np
from embeddings_client import DirectEmbeddingsClient

client = DirectEmbeddingsClient()

def similarity_score(text1, text2):
    embedding1 = client.generate_embedding(text1)
    embedding2 = client.generate_embedding(text2)
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))