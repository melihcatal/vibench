"""Compute cosine similarity between two embedded texts using OpenAI embeddings API."""

import os
from typing import Tuple
import numpy as np
from openai import OpenAI

from embeddings_client import get_openai_client
from embeddings_models import normalize_vector


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))


def embed_and_similarity(
    text_a: str,
    text_b: str,
    model: str = "text-embedding-3-small",
) -> Tuple[float, np.ndarray, np.ndarray]:
    """Embed two texts and compute their cosine similarity.

    Uses OpenAI's text-embedding-3-small model by default.

    Args:
        text_a: First text string.
        text_b: Second text string.
        model: OpenAI embedding model identifier.

    Returns:
        Tuple of (similarity_score, vector_a, vector_b).
    """
    client = get_openai_client()

    response = client.embeddings.create(
        input=[text_a, text_b],
        model=model,
        encoding_format="float",
    )

    vec_a_raw = np.array(response.data[0].embedding, dtype=np.float32)
    vec_b_raw = np.array(response.data[1].embedding, dtype=np.float32)

    vec_a = normalize_vector(vec_a_raw)
    vec_b = normalize_vector(vec_b_raw)

    similarity = cosine_similarity(vec_a, vec_b)
    return similarity, vec_a, vec_b


def similarity_score(
    text_a: str,
    text_b: str,
    model: str = "text-embedding-3-small",
) -> float:
    """Return only the cosine similarity score between two texts."""
    score, _, _ = embed_and_similarity(text_a, text_b, model=model)
    return score


def find_most_similar(
    query: str,
    candidates: list[str],
    model: str = "text-embedding-3-small",
) -> list[tuple[str, float]]:
    """Rank candidates by similarity to query.

    Uses OpenAI embeddings to find the most semantically similar texts.
    """
    client = get_openai_client()

    all_texts = [query] + candidates
    response = client.embeddings.create(
        input=all_texts,
        model=model,
        encoding_format="float",
    )

    query_vec = np.array(response.data[0].embedding, dtype=np.float32)
    query_vec = normalize_vector(query_vec)

    scored = []
    for i, candidate in enumerate(candidates):
        candidate_vec = np.array(response.data[i + 1].embedding, dtype=np.float32)
        candidate_vec = normalize_vector(candidate_vec)
        sim = cosine_similarity(query_vec, candidate_vec)
        scored.append((candidate, sim))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


if __name__ == "__main__":
    text1 = "The cat sat on the mat."
    text2 = "A feline rested on a rug."
    text3 = "The stock market crashed today."

    score, v1, v2 = embed_and_similarity(text1, text2)
    print(f"Similarity between text1 and text2: {score:.4f}")

    score_13, _, _ = embed_and_similarity(text1, text3)
    print(f"Similarity between text1 and text3: {score_13:.4f}")
