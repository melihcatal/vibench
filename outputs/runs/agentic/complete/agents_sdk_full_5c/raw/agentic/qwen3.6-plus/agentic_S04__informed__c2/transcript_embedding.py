"""
[LATER-STEP] Embed transcript segments for semantic retrieval via OpenAI Embeddings API.

Uses OpenAI's embedding service to create vector embeddings for each
transcript segment, enabling semantic search and similarity matching.
Provider: OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY
Model: text-embedding-3-large
"""

import os
from typing import List, Optional, Dict, Any, Tuple

from openai import OpenAI, OpenAIError

from speech_models import TranscriptResponse, Utterance


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"
OPENAI_EMBEDDING_DIMENSIONS = 256


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create and return an OpenAI client.

    Args:
        api_key: Optional OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured openai.OpenAI instance.

    Raises:
        ValueError: If no API key is found.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key."
        )
    return OpenAI(api_key=key)


def embed_segments(
    segments: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Generate OpenAI embeddings for a list of text segments.

    Uses the text-embedding-3-large model for high-quality vector embeddings.

    Args:
        segments: List of text strings to embed.
        model: OpenAI embedding model identifier.
        dimensions: Output embedding dimensions (256, 1024, or 3072 for text-embedding-3-large).
        api_key: OpenAI API key.

    Returns:
        List of dicts with 'text', 'index', 'embedding', and 'model' keys.

    Raises:
        OpenAIError: If the API call fails.
    """
    client = get_openai_client(api_key)

    # OpenAI embedding API has a batch size limit; process in chunks
    batch_size = 2048
    all_results = []

    for batch_start in range(0, len(segments), batch_size):
        batch = segments[batch_start:batch_start + batch_size]

        response = client.embeddings.create(
            model=model,
            input=batch,
            dimensions=dimensions,
        )

        for item in response.data:
            all_results.append({
                "text": batch[item.index],
                "index": batch_start + item.index,
                "embedding": item.embedding,
                "model": item.model,
            })

    return all_results


def embed_transcript(
    transcript: TranscriptResponse,
    granularity: str = "utterance",
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Embed transcript segments from a completed transcription.

    Splits the transcript into segments at the specified granularity
    and generates OpenAI embeddings for each segment.

    Args:
        transcript: Normalized TranscriptResponse.
        granularity: 'utterance', 'sentence', or 'word' for segment boundaries.
        model: OpenAI embedding model.
        dimensions: Embedding dimensions.
        api_key: OpenAI API key.

    Returns:
        List of dicts with embedded segments and metadata.
    """
    segments_with_metadata = _extract_segments(transcript, granularity)
    texts = [seg["text"] for seg in segments_with_metadata]

    # Filter out empty segments
    valid_pairs = [(i, seg, text) for i, (seg, text) in enumerate(zip(segments_with_metadata, texts)) if text.strip()]

    if not valid_pairs:
        return []

    indices = [i for i, _, _ in valid_pairs]
    texts_to_embed = [text for _, _, text in valid_pairs]

    embeddings = embed_segments(
        segments=texts_to_embed,
        model=model,
        dimensions=dimensions,
        api_key=api_key,
    )

    # Reconstruct full result list with metadata
    results = []
    for emb in embeddings:
        orig_idx = indices[emb["index"]]
        metadata = segments_with_metadata[orig_idx]
        results.append({
            "transcript_id": transcript.transcript_id,
            "text": emb["text"],
            "embedding": emb["embedding"],
            "model": emb["model"],
            "dimensions": dimensions,
            "speaker": metadata.get("speaker"),
            "start_ms": metadata.get("start_ms"),
            "end_ms": metadata.get("end_ms"),
            "segment_type": granularity,
            "index": orig_idx,
        })

    return results


def _extract_segments(
    transcript: TranscriptResponse,
    granularity: str,
) -> List[Dict[str, Any]]:
    """
    Extract text segments from transcript at the specified granularity.

    Args:
        transcript: Normalized TranscriptResponse.
        granularity: 'utterance', 'sentence', or 'word'.

    Returns:
        List of segment dicts with text and metadata.
    """
    from speech_models import split_into_sentences

    segments = []

    if granularity == "utterance":
        for utterance in transcript.utterances:
            segments.append({
                "text": utterance.text,
                "speaker": utterance.speaker,
                "start_ms": utterance.start_ms,
                "end_ms": utterance.end_ms,
            })

    elif granularity == "sentence":
        if transcript.utterances:
            current_offset = 0
            for utterance in transcript.utterances:
                sentences = split_into_sentences(utterance.text)
                for sentence in sentences:
                    # Approximate timing within the utterance
                    segments.append({
                        "text": sentence,
                        "speaker": utterance.speaker,
                        "start_ms": utterance.start_ms,
                        "end_ms": utterance.end_ms,
                    })
        else:
            sentences = split_into_sentences(transcript.full_text)
            for sentence in sentences:
                segments.append({
                    "text": sentence,
                    "speaker": None,
                    "start_ms": None,
                    "end_ms": None,
                })

    elif granularity == "word":
        for word in transcript.words:
            segments.append({
                "text": word.text,
                "speaker": word.speaker,
                "start_ms": word.start_ms,
                "end_ms": word.end_ms,
            })

    else:
        raise ValueError(f"Unsupported granularity: {granularity}. Use 'utterance', 'sentence', or 'word'.")

    return segments


def compute_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    import math

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = math.sqrt(sum(a * a for a in embedding_a))
    magnitude_b = math.sqrt(sum(b * b for b in embedding_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_similar_segments(
    query: str,
    embedded_segments: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for segments most similar to a query using OpenAI embeddings.

    Embeds the query and compares it against pre-computed segment embeddings
    using cosine similarity.

    Args:
        query: Search query text.
        embedded_segments: List of pre-embedded segment dicts from embed_transcript().
        top_k: Number of top results to return.
        model: OpenAI embedding model for query embedding.
        dimensions: Embedding dimensions.
        api_key: OpenAI API key.

    Returns:
        Top-k most similar segments with similarity scores.
    """
    # Embed the query
    query_embeddings = embed_segments(
        segments=[query],
        model=model,
        dimensions=dimensions,
        api_key=api_key,
    )
    query_embedding = query_embeddings[0]["embedding"]

    # Compute similarity against all segments
    scored_segments = []
    for seg in embedded_segments:
        similarity = compute_similarity(query_embedding, seg["embedding"])
        scored_segments.append({
            **seg,
            "similarity_score": similarity,
        })

    # Sort by similarity descending
    scored_segments.sort(key=lambda x: x["similarity_score"], reverse=True)

    return scored_segments[:top_k]


def main():
    """CLI entry point for embedding transcript segments."""
    import argparse

    parser = argparse.ArgumentParser(description="Embed transcript segments with OpenAI")
    parser.add_argument("transcript_id", help="Transcript ID to embed")
    parser.add_argument(
        "--granularity",
        choices=["utterance", "sentence", "word"],
        default="utterance",
        help="Segment granularity",
    )
    parser.add_argument("--model", default=OPENAI_EMBEDDING_MODEL, help="OpenAI embedding model")
    parser.add_argument("--dimensions", type=int, default=OPENAI_EMBEDDING_DIMENSIONS, help="Embedding dimensions")
    parser.add_argument("--query", help="Search query for similar segments")
    parser.add_argument("--top-k", type=int, default=5, help="Number of similar results")

    args = parser.parse_args()

    from poll_transcription import poll_transcription

    transcript = poll_transcription(args.transcript_id)

    if args.query:
        embedded = embed_transcript(
            transcript=transcript,
            granularity=args.granularity,
            model=args.model,
            dimensions=args.dimensions,
        )
        results = search_similar_segments(
            query=args.query,
            embedded_segments=embedded,
            top_k=args.top_k,
            model=args.model,
            dimensions=args.dimensions,
        )
        print(f"=== Search Results for: '{args.query}' ===")
        for i, result in enumerate(results):
            print(f"\n{i+1}. [{result.get('speaker', '?')}] (similarity: {result['similarity_score']:.4f})")
            print(f"   {result['text']}")
    else:
        embedded = embed_transcript(
            transcript=transcript,
            granularity=args.granularity,
            model=args.model,
            dimensions=args.dimensions,
        )
        print(f"=== Embedded {len(embedded)} segments ===")
        print(f"Model: {args.model}")
        print(f"Dimensions: {args.dimensions}")
        print(f"Segment type: {args.granularity}")

    return embedded


if __name__ == "__main__":
    main()
