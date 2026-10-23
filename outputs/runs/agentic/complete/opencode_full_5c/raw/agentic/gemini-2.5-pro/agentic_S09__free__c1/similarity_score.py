import numpy as np
from embeddings_client import get_cohere_client
from embeddings_models import SimilarityResponse


def calculate_similarity(text1: str, text2: str) -> SimilarityResponse:
    """
    Computes cosine similarity between two embedded texts using Cohere.
    """
    cohere_client = get_cohere_client()
    embeddings = cohere_client.embed(
        texts=[text1, text2], model="embed-english-v3.0", input_type="search_document"
    ).embeddings

    embedding1 = np.array(embeddings[0])
    embedding2 = np.array(embeddings[1])

    cosine_similarity = np.dot(embedding1, embedding2) / (
        np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    )

    return SimilarityResponse(similarity=float(cosine_similarity))
