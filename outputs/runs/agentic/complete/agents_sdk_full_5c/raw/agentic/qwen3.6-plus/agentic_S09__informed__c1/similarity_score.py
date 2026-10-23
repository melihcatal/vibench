"""Computes cosine similarity between two embedded texts using OpenAI Embeddings API.

Embeds both input texts with the OpenAI text-embedding-3-small model and
calculates their cosine similarity.
"""

import os
from typing import Tuple, List

from embeddings_client import get_openai_client, create_batch_embeddings, get_embedding_model
from embeddings_models import cosine_similarity, SimilarityResult, build_similarity_result


def compute_similarity(
    text_a: str,
    text_b: str,
    model: str = None,
) -> SimilarityResult:
    """Compute cosine similarity between two text strings.

    Args:
        text_a: First text string.
        text_b: Second text string.
        model: OpenAI embedding model ID (defaults to OPENAI_EMBEDDING_MODEL env var).

    Returns:
        SimilarityResult with score and input texts.
    """
    client = get_openai_client()
    model_id = model or get_embedding_model()

    response = client.embeddings.create(
        input=[text_a, text_b],
        model=model_id,
    )

    embedding_a = response.data[0].embedding
    embedding_b = response.data[1].embedding

    return build_similarity_result(text_a, text_b, embedding_a, embedding_b)


def similarity_raw_score(
    text_a: str,
    text_b: str,
    model: str = None,
) -> float:
    """Return raw cosine similarity score between two texts.

    Args:
        text_a: First text string.
        text_b: Second text string.
        model: OpenAI embedding model ID.

    Returns:
        Cosine similarity score in [-1, 1].
    """
    result = compute_similarity(text_a, text_b, model=model)
    return result.score


def main():
    text_a = os.environ.get("SIM_TEXT_A", "I love programming in Python")
    text_b = os.environ.get("SIM_TEXT_B", "Python programming is my favorite")
    model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    result = compute_similarity(text_a, text_b, model=model)
    print(f"Model: {model}")
    print(f"Text A: {result.text_a}")
    print(f"Text B: {result.text_b}")
    print(f"Cosine similarity: {result.score:.6f}")


if __name__ == "__main__":
    main()
