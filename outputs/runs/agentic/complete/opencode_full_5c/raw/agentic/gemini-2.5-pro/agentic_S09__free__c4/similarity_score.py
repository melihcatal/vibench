import numpy as np
from embeddings_client import get_cohere_client


def similarity_score(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between two embedded texts using Cohere.
    """
    cohere_client = get_cohere_client()
    model = "embed-english-v3.0"

    response = cohere_client.embed(
        texts=[text1, text2], model=model, input_type="search_document"
    )

    emb1 = np.array(response.embeddings[0])
    emb2 = np.array(response.embeddings[1])

    cosine_similarity = np.dot(emb1, emb2) / (
        np.linalg.norm(emb1) * np.linalg.norm(emb2)
    )
    return float(cosine_similarity)
