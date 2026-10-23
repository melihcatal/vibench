"""
output_embedding.py — Embed model outputs for clustering or retrieval.

Uses the OpenAI Embeddings API (api.openai.com) with the
text-embedding-3-small model to produce vector representations of text.
"""

from __future__ import annotations

from typing import List, Optional

from model_client import generate_embeddings, resolve_model
from model_models import EmbeddingRequest, EmbeddingResponse

# Concrete OpenAI model identifier for embeddings
EMBEDDING_MODEL = resolve_model("text-embedding-3-small")  # text-embedding-3-small


def embed_text(
    text: str,
    model: Optional[str] = None,
) -> List[float]:
    """
    Generate an embedding vector for a single text using OpenAI's
    text-embedding-3-small model.

    Parameters
    ----------
    text : str
        The text to embed.
    model : str, optional
        Concrete OpenAI embedding model ID (defaults to text-embedding-3-small).

    Returns
    -------
    list of float
        The embedding vector (1536 dimensions for text-embedding-3-small).
    """
    target_model = model or EMBEDDING_MODEL
    request = EmbeddingRequest(input_text=text, model=target_model)
    response: EmbeddingResponse = generate_embeddings(request)
    return response.embedding


def embed_texts_batch(
    texts: List[str],
    model: Optional[str] = None,
) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using the OpenAI Embeddings API.

    Each text is embedded individually via the text-embedding-3-small model.

    Parameters
    ----------
    texts : list of str
        Texts to embed.
    model : str, optional
        Concrete OpenAI embedding model ID.

    Returns
    -------
    list of list of float
        Embedding vectors corresponding to each input text.
    """
    embeddings: List[List[float]] = []
    for text in texts:
        embeddings.append(embed_text(text, model=model))
    return embeddings


def embed_model_outputs(
    outputs: List[str],
    model: Optional[str] = None,
) -> dict:
    """
    Embed a list of model-generated outputs for downstream clustering
    or similarity search.

    Parameters
    ----------
    outputs : list of str
        Model-generated text outputs to embed.
    model : str, optional
        Concrete OpenAI embedding model ID.

    Returns
    -------
    dict
        Dictionary containing the embeddings list, model name, and dimension.
    """
    target_model = model or EMBEDDING_MODEL
    vectors = embed_texts_batch(outputs, model=target_model)
    return {
        "model": target_model,
        "dimension": len(vectors[0]) if vectors else 0,
        "embeddings": vectors,
        "count": len(vectors),
    }


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Parameters
    ----------
    vec_a : list of float
        First vector.
    vec_b : list of float
        Second vector.

    Returns
    -------
    float
        Cosine similarity in range [-1, 1].
    """
    import math

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_most_similar(
    query_text: str,
    candidate_texts: List[str],
    top_k: int = 5,
    model: Optional[str] = None,
) -> List[dict]:
    """
    Find the top-k most similar candidate texts to a query using OpenAI
    text-embedding-3-small embeddings and cosine similarity.

    Parameters
    ----------
    query_text : str
        Query text to match against.
    candidate_texts : list of str
        Pool of candidate texts.
    top_k : int
        Number of results to return.
    model : str, optional
        Concrete OpenAI embedding model ID.

    Returns
    -------
    list of dict
        Sorted results with text, score, and index.
    """
    query_vec = embed_text(query_text, model=model)
    candidate_vecs = embed_texts_batch(candidate_texts, model=model)

    scored: List[dict] = []
    for idx, candidate_vec in enumerate(candidate_vecs):
        score = cosine_similarity(query_vec, candidate_vec)
        scored.append({
            "text": candidate_texts[idx],
            "score": score,
            "index": idx,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    texts = [
        "Machine learning enables computers to learn from data.",
        "Natural language processing helps computers understand human language.",
        "The quick brown fox jumps over the lazy dog.",
    ]
    result = embed_model_outputs(texts)
    print(f"Embedded {result['count']} texts using {result['model']}")
    print(f"Vector dimension: {result['dimension']}")
