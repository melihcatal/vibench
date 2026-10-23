import numpy as np

from google import genai


def similarity_score(embedding1, embedding2):
    cosine_similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return cosine_similarity