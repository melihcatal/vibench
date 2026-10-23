"""
Later-step: Embed model outputs for clustering or retrieval.

Provider: Cohere Embed API
SDK: cohere
Auth: COHERE_API_KEY
Model: embed-english-v3.0
"""

import os
from typing import Optional, List, Dict, Any

import cohere


def _get_cohere_client() -> cohere.Client:
    """
    Create a Cohere client using the COHERE_API_KEY environment variable.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required.")
    return cohere.Client(api_key)


def embed_text(
    text: str,
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
    truncate: str = "END",
) -> Dict[str, Any]:
    """
    Generate an embedding for a single text string using the Cohere Embed API.

    Args:
        text: The text to embed.
        model: The Cohere embedding model identifier. Defaults to embed-english-v3.0.
        input_type: Type of input for embedding ("search_document", "search_query",
                    "classification", "clustering").
        truncate: How to handle inputs longer than the max token length ("NONE", "START", "END").

    Returns:
        A dict containing the embedding vector and metadata.
    """
    client = _get_cohere_client()

    response = client.embed(
        texts=[text],
        model=model,
        input_type=input_type,
        truncate=truncate,
    )

    embeddings = response.embeddings
    if not embeddings or len(embeddings) == 0:
        raise ValueError("Cohere API returned no embeddings.")

    return {
        "embedding": embeddings[0],
        "model_used": model,
        "input_type": input_type,
        "raw_response": response,
    }


def embed_texts_batch(
    texts: List[str],
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
    truncate: str = "END",
) -> Dict[str, Any]:
    """
    Generate embeddings for multiple texts in a single batch via Cohere.

    Args:
        texts: List of text strings to embed.
        model: The Cohere embedding model identifier.
        input_type: Type of input for embedding.
        truncate: How to handle inputs longer than the max token length.

    Returns:
        A dict containing the list of embedding vectors and metadata.
    """
    client = _get_cohere_client()

    response = client.embed(
        texts=texts,
        model=model,
        input_type=input_type,
        truncate=truncate,
    )

    embeddings = response.embeddings or []
    return {
        "embeddings": embeddings,
        "model_used": model,
        "input_type": input_type,
        "count": len(embeddings),
        "raw_response": response,
    }


def compute_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    import math

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def find_most_similar(
    query_text: str,
    candidate_texts: List[str],
    model: str = "embed-english-v3.0",
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """
    Find the most similar candidate texts to a query using Cohere embeddings.

    Args:
        query_text: The query text.
        candidate_texts: List of candidate texts to compare against.
        model: The Cohere embedding model identifier.
        top_k: Number of top results to return.

    Returns:
        A sorted list of dicts with 'text', 'score', and 'embedding'.
    """
    query_result = embed_text(query_text, model=model, input_type="search_query")
    candidate_result = embed_texts_batch(
        candidate_texts, model=model, input_type="search_document"
    )

    query_vec = query_result["embedding"]
    candidate_vecs = candidate_result["embeddings"]

    scored = []
    for i, vec in enumerate(candidate_vecs):
        similarity = compute_cosine_similarity(query_vec, vec)
        scored.append({
            "text": candidate_texts[i],
            "score": similarity,
            "embedding": vec,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
