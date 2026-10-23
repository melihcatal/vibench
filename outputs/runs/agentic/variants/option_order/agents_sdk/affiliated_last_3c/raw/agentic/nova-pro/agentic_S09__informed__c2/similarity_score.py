import numpy as np
from scipy.spatial.distance import cosine

def compute_similarity(embedding1, embedding2):
    return 1 - cosine(embedding1, embedding2)