from typing import List
import numpy as np
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_vector


def get_similarity_score(text_a: str, text_b: str) -> float:
    client = get_embeddings_client()

    embeddings = client.get_embeddings([text_a, text_b])

    embedding_a = normalize_vector(
        [e.values for e in embeddings if e.text == text_a][0]
    )
    embedding_b = normalize_vector(
        [e.values for e in embeddings if e.text == text_b][0]
    )

    similarity = np.dot(embedding_a, embedding_b)
    return float(similarity)


if __name__ == "__main__":
    score = get_similarity_score(
        "I am a software engineer.", "I write code for a living."
    )
    print(f"Similarity score: {score}")
