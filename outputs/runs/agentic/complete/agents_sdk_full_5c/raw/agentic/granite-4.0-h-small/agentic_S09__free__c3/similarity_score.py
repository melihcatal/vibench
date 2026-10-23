import numpy as np
from embeddings_client import get_client
from embeddings_models import normalize_embedding

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec_a, vec_b: Embedding vectors as lists of floats.

    Returns:
        Similarity score between -1 and 1.
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def score_embeddings(text_a: str, text_b: str) -> float:
    """Embed two texts and return their cosine similarity.

    Uses the Direct Embeddings API via the helper client.
    """
    client = get_client()
    model_id = "text-embedding-ada-002"
    response = client.create_embedding(
        model=model_id,
        input=[text_a, text_b],  # batch of two texts
    )
    embeddings = response["embeddings"]
    vec_a = normalize_embedding(embeddings[0])
    vec_b = normalize_embedding(embeddings[1])
    return cosine_similarity(vec_a, vec_b)
