"""
similarity_score.py - Computes cosine similarity between two embedded texts.

Provider: OpenAI Embeddings API
Model: text-embedding-3-small
SDK: openai
Auth: OPENAI_API_KEY
"""

from embeddings_client import get_openai_client, resolve_model
from embeddings_models import EmbeddingRequest, parse_openai_embedding_response, cosine_similarity


def compute_similarity(
    text_a: str,
    text_b: str,
    model: str | None = None,
) -> float:
    """Compute cosine similarity between two texts via OpenAI Embeddings API.

    Both texts are embedded using the same OpenAI model to ensure
    vector space compatibility, then cosine similarity is computed.

    Args:
        text_a: First input text.
        text_b: Second input text.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).

    Returns:
        Cosine similarity score in the range [-1, 1].
    """
    client = get_openai_client()
    resolved_model = resolve_model(model)

    request = EmbeddingRequest(
        input=[text_a, text_b],
        model=resolved_model,
    )

    response = client.embeddings.create(**request.to_openai_params())
    parsed = parse_openai_embedding_response(response)

    if len(parsed.vectors) < 2:
        raise RuntimeError("Expected two embedding vectors from OpenAI Embeddings API")

    vec_a = parsed.vectors[0].vector
    vec_b = parsed.vectors[1].vector

    return cosine_similarity(vec_a, vec_b)


def main() -> None:
    pair_1 = (
        "The quick brown fox jumps over the lazy dog",
        "A fast brown fox leaps over a sleepy canine",
    )
    score_1 = compute_similarity(*pair_1)
    print(f"Similarity (semantically related): {score_1:.4f}")

    pair_2 = (
        "Python is a popular programming language for data science",
        "Freshly baked bread smells wonderful in the morning",
    )
    score_2 = compute_similarity(*pair_2)
    print(f"Similarity (unrelated): {score_2:.4f}")


if __name__ == "__main__":
    main()
