import numpy as np
from embeddings_client import get_embeddings_client

def similarity_score(embedding1, embedding2):
    return np.dot(embedding1, embedding2)/(np.linalg.norm(embedding1)*np.linalg.norm(embedding2))