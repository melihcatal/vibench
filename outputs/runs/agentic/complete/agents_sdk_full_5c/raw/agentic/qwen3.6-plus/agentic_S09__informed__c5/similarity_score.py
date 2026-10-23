"""
[SAME-SCENARIO] Computes cosine similarity between two embedded texts.
Provider: OpenAI Embeddings API (text-embedding-3-small)
SDK: openai
Auth: OPENAI_API_KEY
"""

from typing import Optional

from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import cosine_similarity, normalize_vector


def similarity_score(
    text_a: str,
    text_b: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> float:
    """
    Compute the cosine similarity between two texts using OpenAI embeddings.

    Args:
        text_a: First input text.
        text_b: Second input text.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        api_key: Optional OpenAI API key (falls back to OPENAI_API_KEY env var).

    Returns:
        Cosine similarity score in range [-1.0, 1.0].
    """
    client = get_openai_client(api_key=api_key)
    model_name = model or get_embedding_model()

    response = client.embeddings.create(
        model=model_name,
        input=[text_a, text_b],
        encoding_format="float",
    )

    vec_a = response.data[0].embedding
    vec_b = response.data[1].embedding

    vec_a = normalize_vector(vec_a)
    vec_b = normalize_vector(vec_b)

    return cosine_similarity(vec_a, vec_b)


def similarity_score_from_vectors(
    vec_a: list,
    vec_b: list,
) -> float:
    """
    Compute cosine similarity from pre-computed embedding vectors.

    Args:
        vec_a: First embedding vector (list of floats).
        vec_b: Second embedding vector (list of floats).

    Returns:
        Cosine similarity score.
    """
    return cosine_similarity(vec_a, vec_b)


if __name__ == "__main__":
    t1 = "A happy dog runs in the park."
    t2 = "A joyful canine sprints outdoors."
    score = similarity_score(t1, t2)
    print(f"Text A: {t1}")
    print(f"Text B: {t2}")
    print(f"Cosine similarity: {score:.4f}")
