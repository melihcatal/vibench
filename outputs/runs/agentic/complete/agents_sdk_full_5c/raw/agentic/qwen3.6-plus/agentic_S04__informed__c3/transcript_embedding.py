"""
Embed transcript segments for semantic retrieval using OpenAI Embeddings API.

Generates vector embeddings for transcript segments using OpenAI's
text-embedding-3-small or text-embedding-3-large models.
Requires OPENAI_API_KEY environment variable.
"""

import os
import sys
from typing import List, Optional, Dict, Any, Union

from openai import OpenAI


# OpenAI provider identifiers
PROVIDER = "OpenAI"
PROVIDER_MODEL = "text-embedding-3-small"
PROVIDER_API_HOST = "api.openai.com"


class TranscriptEmbedder:
    """Wrapper for OpenAI text embeddings for transcript segments."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = PROVIDER_MODEL,
    ):
        """
        Initialize OpenAI embedding client.

        Args:
            api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.
            model: Embedding model identifier (default: text-embedding-3-small).
        """
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError(
                "OPENAI_API_KEY environment variable must be set "
                "to use OpenAI Embeddings API"
            )
        self.client = OpenAI(api_key=key)
        self.model = model

    def embed_text(
        self,
        text: str,
        dimensions: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate embedding for a single text segment.

        Args:
            text: Text to embed.
            dimensions: Optional output dimensionality (for text-embedding-3 models).

        Returns:
            Dict with embedding vector and metadata.
        """
        params: Dict[str, Any] = {
            "model": self.model,
            "input": text,
        }
        if dimensions is not None:
            params["dimensions"] = dimensions

        response = self.client.embeddings.create(**params)

        embedding = response.data[0].embedding

        return {
            "text": text,
            "embedding": embedding,
            "model": self.model,
            "provider": PROVIDER,
            "dimensions": len(embedding),
            "usage_tokens": response.usage.total_tokens,
        }

    def embed_segments(
        self,
        segments: List[str],
        dimensions: Optional[int] = None,
        batch_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for multiple transcript segments.

        Args:
            segments: List of text segments to embed.
            dimensions: Optional output dimensionality.
            batch_size: Number of segments per API request.

        Returns:
            List of dicts with text and embedding vectors.
        """
        results = []

        for i in range(0, len(segments), batch_size):
            batch = segments[i : i + batch_size]

            params: Dict[str, Any] = {
                "model": self.model,
                "input": batch,
            }
            if dimensions is not None:
                params["dimensions"] = dimensions

            response = self.client.embeddings.create(**params)

            for j, data in enumerate(response.data):
                results.append({
                    "text": batch[j],
                    "embedding": data.embedding,
                    "model": self.model,
                    "provider": PROVIDER,
                    "dimensions": len(data.embedding),
                    "index": i + j,
                })

        return results

    def embed_transcript(
        self,
        transcript_text: str,
        segment_size: int = 500,
        overlap: int = 50,
        dimensions: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Split and embed a full transcript into overlapping segments.

        Args:
            transcript_text: Full transcript text.
            segment_size: Maximum characters per segment.
            overlap: Character overlap between segments.
            dimensions: Optional output dimensionality.

        Returns:
            List of dicts with segment text and embeddings.
        """
        # Simple chunking by character count
        segments = []
        start = 0
        while start < len(transcript_text):
            end = min(start + segment_size, len(transcript_text))
            segment = transcript_text[start:end]
            segments.append(segment)
            start = end - overlap if end < len(transcript_text) else len(transcript_text)

        return self.embed_segments(segments, dimensions=dimensions)


def generate_transcript_embeddings(
    segments: List[str],
    model: str = PROVIDER_MODEL,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for transcript segments using OpenAI.

    Args:
        segments: List of transcript text segments.
        model: OpenAI embedding model (default: text-embedding-3-small).
        api_key: Optional OpenAI API key override.

    Returns:
        List of dicts with segments and their embedding vectors.
    """
    embedder = TranscriptEmbedder(api_key=api_key, model=model)
    return embedder.embed_segments(segments)


def embed_transcript_for_retrieval(
    transcript_text: str,
    model: str = PROVIDER_MODEL,
    api_key: Optional[str] = None,
    dimensions: int = 256,
) -> Dict[str, Any]:
    """
    Prepare a transcript for semantic retrieval by embedding it.

    Args:
        transcript_text: Full transcript text.
        model: OpenAI embedding model.
        api_key: Optional OpenAI API key override.
        dimensions: Output embedding dimensions.

    Returns:
        Dict with segments and their embeddings for storage/indexing.
    """
    embedder = TranscriptEmbedder(api_key=api_key, model=model)
    embeddings = embedder.embed_transcript(
        transcript_text,
        segment_size=500,
        overlap=50,
        dimensions=dimensions,
    )

    return {
        "segments": embeddings,
        "provider": PROVIDER,
        "model": model,
        "dimensions": dimensions,
        "segment_count": len(embeddings),
    }


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec1: First embedding vector.
        vec2: Second embedding vector.

    Returns:
        Cosine similarity score (0.0 to 1.0).
    """
    import math

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


if __name__ == "__main__":
    # Example usage
    sample_segments = [
        "The meeting discussed Q3 financial results and revenue growth.",
        "Action items were assigned to team members for follow-up.",
        "The product launch timeline was extended by two weeks.",
    ]

    results = generate_transcript_embeddings(sample_segments)
    for r in results:
        print(f"Text: {r['text'][:50]}...")
        print(f"Dimensions: {r['dimensions']}")
        print(f"First 5 values: {r['embedding'][:5]}")
        print()
