import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def normalize_embedding_response(response):
    return np.array(response.embedding)