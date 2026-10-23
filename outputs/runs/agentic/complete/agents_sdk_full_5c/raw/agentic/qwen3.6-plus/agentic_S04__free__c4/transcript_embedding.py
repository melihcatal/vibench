"""
Embed transcript segments for semantic retrieval using the OpenAI Embeddings API.

Generates vector embeddings for transcript segments to enable semantic
search and similarity-based retrieval.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_EMBEDDING_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def embed_text(text: str, dimensions: Optional[int] = None) -> Dict[str, Any]:
    """
    Generate an embedding vector for a single text using OpenAI text-embedding-3-small.

    Parameters
    ----------
    text : str
        Text to embed.
    dimensions : int, optional
        Number of dimensions for the embedding (model supports up to 1536).

    Returns
    -------
    dict
        Contains the embedding vector and metadata.
    """
    api_key = get_openai_api_key()

    payload = {
        "input": text,
        "model": OPENAI_EMBEDDING_MODEL,
    }

    if dimensions is not None:
        payload["dimensions"] = dimensions

    response = requests.post(
        OPENAI_EMBEDDING_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    result = response.json()

    embedding_data = result["data"][0]
    return {
        "text": text,
        "embedding": embedding_data["embedding"],
        "model": embedding_data["model"],
        "index": embedding_data["index"],
    }


def embed_segments(
    segments: List[str],
    dimensions: Optional[int] = None,
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for multiple transcript segments using OpenAI Embeddings API.

    Parameters
    ----------
    segments : list[str]
        List of transcript text segments to embed.
    dimensions : int, optional
        Number of embedding dimensions.
    batch_size : int
        Maximum segments per API request.

    Returns
    -------
    list[dict]
        Each dict contains segment index, text, and embedding vector.
    """
    api_key = get_openai_api_key()
    all_results = []

    for batch_start in range(0, len(segments), batch_size):
        batch = segments[batch_start:batch_start + batch_size]

        payload = {
            "input": batch,
            "model": OPENAI_EMBEDDING_MODEL,
        }

        if dimensions is not None:
            payload["dimensions"] = dimensions

        response = requests.post(
            OPENAI_EMBEDDING_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

        for item in result["data"]:
            all_results.append({
                "segment_index": batch_start + item["index"],
                "text": batch[item["index"]] if item["index"] < len(batch) else "",
                "embedding": item["embedding"],
                "model": item["model"],
            })

    return all_results


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def search_similar_segments(
    query: str,
    segments: List[str],
    embeddings: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Find segments most similar to a query using OpenAI embeddings and cosine similarity.
    """
    query_result = embed_text(query)
    query_embedding = query_result["embedding"]

    scored = []
    for emb in embeddings:
        sim = cosine_similarity(query_embedding, emb["embedding"])
        scored.append({
            "segment_index": emb["segment_index"],
            "text": emb["text"],
            "similarity": sim,
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def main() -> None:
    parser = argparse.ArgumentParser(description="Embed transcript segments with OpenAI")
    parser.add_argument("transcript", help="Transcript text or JSON file path")
    parser.add_argument("--dimensions", type=int, help="Embedding dimensions")
    parser.add_argument("--query", help="Search query for similarity ranking")
    parser.add_argument("--top-k", type=int, default=5, help="Number of similar results")
    parser.add_argument("--input-format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.input_format == "json":
        with open(args.transcript) as f:
            data = json.load(f)
            if isinstance(data, list):
                segments = [seg.get("text", str(seg)) for seg in data]
            else:
                segments = [data.get("text", str(data))]
    else:
        try:
            with open(args.transcript) as f:
                text = f.read()
        except FileNotFoundError:
            text = args.transcript
        segments = [text]

    embeddings = embed_segments(segments, dimensions=args.dimensions)

    if args.query:
        results = search_similar_segments(args.query, segments, embeddings, top_k=args.top_k)
        print(json.dumps(results, indent=2))
    else:
        # Return embeddings without the full vector for readability
        summary = []
        for emb in embeddings:
            summary.append({
                "segment_index": emb["segment_index"],
                "text": emb["text"][:100],
                "embedding_dimension": len(emb["embedding"]),
                "model": emb["model"],
            })
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
