import numpy as np
from embeddings_client import get_cohere_client


def similarity_score(text1: str, text2: str):
    cohere_client = get_cohere_client()
    response = cohere_client.embed(
        texts=[text1, text2], model="embed-english-v3.0", input_type="search_document"
    )
    vec1 = np.array(response.embeddings[0])
    vec2 = np.array(response.embeddings[1])

    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return similarity
