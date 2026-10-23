"""
transcript_embedding.py - Embed transcript segments for semantic retrieval.

Uses OpenAI's text embedding API to convert transcript segments into dense
vector representations for semantic search, clustering, and retrieval.

OpenAI Embeddings API: https://api.openai.com/v1/embeddings
Model: text-embedding-3-small
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from typing import List, Dict, Any, Optional

import requests

from speech_models import SegmentEmbedding

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# OpenAI-specific embedding configuration
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_EMBEDDINGS_ENDPOINT = f"{OPENAI_API_BASE}/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = 1536


class OpenAIConfig:
    """OpenAI API configuration."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )
        self.model = OPENAI_EMBEDDING_MODEL
        self.dimensions = OPENAI_EMBEDDING_DIMENSIONS
        self.timeout = 30

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


def embed_segments(
    segments: List[str],
    config: Optional[OpenAIConfig] = None,
    batch_size: int = 100,
) -> List[SegmentEmbedding]:
    """
    Embed transcript segments using OpenAI's text-embedding-3-small model.

    Args:
        segments: List of text segments to embed
        config: OpenAI configuration
        batch_size: Number of segments per API request (max 2048 for OpenAI)

    Returns:
        List of SegmentEmbedding objects with vectors
    """
    config = config or OpenAIConfig()
    embeddings = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]

        payload = {
            "model": OPENAI_EMBEDDING_MODEL,  # OpenAI text-embedding-3-small
            "input": batch,
            "dimensions": config.dimensions,
        }

        response = requests.post(
            OPENAI_EMBEDDINGS_ENDPOINT,
            headers=config.headers,
            json=payload,
            timeout=config.timeout,
        )
        response.raise_for_status()
        result = response.json()

        for j, item in enumerate(result["data"]):
            segment_idx = i + j
            embeddings.append(SegmentEmbedding(
                segment_index=segment_idx,
                text=batch[j],
                embedding=item["embedding"],
                model=OPENAI_EMBEDDING_MODEL,
            ))

    logger.info(
        "Embedded %d segments using OpenAI %s (%d dimensions)",
        len(embeddings),
        OPENAI_EMBEDDING_MODEL,
        config.dimensions,
    )

    return embeddings


def embed_transcript_from_json(
    transcript_json_path: str,
    config: Optional[OpenAIConfig] = None,
) -> List[SegmentEmbedding]:
    """
    Load transcript from JSON and embed all segments.

    Args:
        transcript_json_path: Path to transcript JSON file
        config: OpenAI configuration

    Returns:
        List of SegmentEmbedding objects
    """
    with open(transcript_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = []
    for seg in data.get("segments", []):
        if isinstance(seg, dict):
            text = seg.get("text", "")
            speaker = seg.get("speaker", "")
            # Include speaker context in embedding for better retrieval
            if speaker:
                text = f"[Speaker {speaker}] {text}"
        else:
            text = str(seg)
        segments.append(text)

    return embed_segments(segments, config)


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    import math

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = math.sqrt(sum(a * a for a in embedding_a))
    magnitude_b = math.sqrt(sum(b * b for b in embedding_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_segments(
    query: str,
    embeddings: List[SegmentEmbedding],
    top_k: int = 5,
    config: Optional[OpenAIConfig] = None,
) -> List[Dict[str, Any]]:
    """
    Search for relevant transcript segments using semantic similarity.

    Embeds the query using OpenAI text-embedding-3-small and finds
    the most similar transcript segments.

    Args:
        query: Search query text
        embeddings: List of pre-computed segment embeddings
        top_k: Number of results to return
        config: OpenAI configuration

    Returns:
        List of results with segment text and similarity scores
    """
    config = config or OpenAIConfig()

    # Embed query using OpenAI
    payload = {
        "model": OPENAI_EMBEDDING_MODEL,
        "input": query,
        "dimensions": config.dimensions,
    }

    response = requests.post(
        OPENAI_EMBEDDINGS_ENDPOINT,
        headers=config.headers,
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    result = response.json()

    query_embedding = result["data"][0]["embedding"]

    # Compute similarities
    scored = []
    for emb in embeddings:
        similarity = compute_similarity(query_embedding, emb.embedding)
        scored.append({
            "segment_index": emb.segment_index,
            "text": emb.text,
            "similarity": similarity,
        })

    # Sort by similarity descending
    scored.sort(key=lambda x: x["similarity"], reverse=True)

    return scored[:top_k]


def save_embeddings(
    embeddings: List[SegmentEmbedding],
    output_path: str,
):
    """Save embeddings to JSON file for later retrieval."""
    data = [
        {
            "segment_index": e.segment_index,
            "text": e.text,
            "embedding": e.embedding,
            "model": e.model,
        }
        for e in embeddings
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    logger.info("Saved %d embeddings to %s", len(embeddings), output_path)


def format_embedding_output(embeddings: List[SegmentEmbedding]) -> str:
    """Format embedding results for display."""
    lines = [
        f"Segment Embeddings (OpenAI {OPENAI_EMBEDDING_MODEL})",
        f"Total segments: {len(embeddings)}",
        f"Dimensions: {OPENAI_EMBEDDING_DIMENSIONS}",
        "=" * 80,
    ]

    for emb in embeddings:
        # Show first few dimensions as example
        preview = ", ".join(f"{v:.4f}" for v in emb.embedding[:5])
        lines.append(
            f"  Segment {emb.segment_index}: [{preview}, ...] ({len(emb.embedding)} dims)"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Embed transcript segments using OpenAI text-embedding-3-small")
    parser.add_argument("transcript_json", help="Path to transcript JSON file")
    parser.add_argument("--search", help="Search query for semantic retrieval")
    parser.add_argument("--top-k", type=int, default=5, help="Number of search results")
    parser.add_argument("--output", help="Save embeddings to JSON file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    embeddings = embed_transcript_from_json(args.transcript_json)

    if args.search:
        results = search_segments(args.search, embeddings, args.top_k)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Search results for: '{args.search}'\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. (similarity: {result['similarity']:.4f})")
                print(f"   Segment {result['segment_index']}: {result['text'][:150]}...\n")
    elif args.output:
        save_embeddings(embeddings, args.output)
        print(f"Saved {len(embeddings)} embeddings to {args.output}")
    elif args.json:
        output = [
            {
                "segment_index": e.segment_index,
                "text": e.text,
                "embedding": e.embedding,
                "model": e.model,
            }
            for e in embeddings
        ]
        print(json.dumps(output, indent=2))
    else:
        print(format_embedding_output(embeddings))


if __name__ == "__main__":
    main()
