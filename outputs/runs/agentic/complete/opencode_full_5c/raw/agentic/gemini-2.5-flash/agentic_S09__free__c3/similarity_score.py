import numpy as np
from embeddings_client import get_cohere_client
from embeddings_models import COHERE_EMBEDDING_MODEL, extract_embeddings


def similarity_score(text1: str, text2: str) -> float:
    """Computes the cosine similarity between two embedded texts using Cohere embeddings."""
    co = get_cohere_client()
    response = co.embed(
        texts=[text1, text2], model=COHERE_EMBEDDING_MODEL, input_type="search_document"
    )
    embeddings = extract_embeddings(response)
    if len(embeddings) != 2:
        raise ValueError("Could not generate embeddings for both texts.")

    vec1 = np.array(embeddings[0])
    vec2 = np.array(embeddings[1])

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    return dot_product / (norm_vec1 * norm_vec2)
