import numpy as np
from typing import List
from embeddings_client import get_openai_embedding_client, OPENAI_EMBEDDING_MODEL

def _get_embedding(text: str) -> List[float]:
    client = get_openai_embedding_client()
    response = client.embeddings.create(
        input=[text],
        model=OPENAI_EMBEDDING_MODEL
    )
    return response.data[0].embedding

def compute_cosine_similarity(text1: str, text2: str) -> float:
    embedding1 = _get_embedding(text1)
    embedding2 = _get_embedding(text2)

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)
