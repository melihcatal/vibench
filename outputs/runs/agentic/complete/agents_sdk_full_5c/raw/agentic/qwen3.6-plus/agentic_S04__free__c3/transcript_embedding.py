"""
Embed transcript segments for semantic retrieval using OpenAI Embeddings API.

Provider: OpenAI API
SDK: openai
Model: text-embedding-3-large
Endpoint: api.openai.com
Environment: OPENAI_API_KEY
"""

from typing import List, Optional, Dict, Any, Tuple

from openai import OpenAI

from speech_models import TranscriptSegment


def embed_segments(
    segments: List[TranscriptSegment],
    model: str = "text-embedding-3-large",
    api_key: Optional[str] = None,
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for transcript segments for semantic search.

    Args:
        segments: List of TranscriptSegment to embed
        model: OpenAI embedding model (text-embedding-3-large or text-embedding-3-small)
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        batch_size: Number of segments to embed per API call

    Returns:
        List of dicts with segment index, text, and embedding vector.
    """
    client = OpenAI(api_key=api_key)

    results = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]
        texts = [seg.transcript for seg in batch]

        response = client.embeddings.create(
            model=model,
            input=texts,
            encoding_format="float",
        )

        for j, embedding_obj in enumerate(response.data):
            segment_idx = i + j
            results.append({
                "segment_index": segment_idx,
                "text": texts[j],
                "embedding": embedding_obj.embedding,
                "model": model,
                "speaker_tag": batch[j].speaker_tag,
                "confidence": batch[j].confidence,
            })

    return results


def embed_and_index(
    segments: List[TranscriptSegment],
    index: Optional[Dict[str, Any]] = None,
    model: str = "text-embedding-3-large",
    api_key: Optional[str] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Embed segments and build a simple in-memory search index.

    Args:
        segments: Transcript segments
        index: Existing index to update, or None to create new
        model: Embedding model to use
        api_key: OpenAI API key

    Returns:
        Tuple of (index, embeddings)
    """
    if index is None:
        index = {
            "segments": [],
            "embeddings": [],
            "model": model,
            "total_segments": 0,
        }

    embeddings = embed_segments(segments, model=model, api_key=api_key)

    for emb in embeddings:
        index["segments"].append({
            "index": emb["segment_index"],
            "text": emb["text"],
            "speaker_tag": emb["speaker_tag"],
            "confidence": emb["confidence"],
        })
        index["embeddings"].append(emb["embedding"])

    index["total_segments"] = len(index["segments"])

    return index, embeddings


def search_similar_segments(
    query: str,
    index: Dict[str, Any],
    top_k: int = 5,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for segments semantically similar to a query.

    Args:
        query: Search query text
        index: Embedding index built by embed_and_index
        top_k: Number of results to return
        api_key: OpenAI API key

    Returns:
        List of matching segments with similarity scores.
    """
    client = OpenAI(api_key=api_key)

    # Embed the query
    query_response = client.embeddings.create(
        model=index["model"],
        input=[query],
        encoding_format="float",
    )
    query_embedding = query_response.data[0].embedding

    # Compute cosine similarity with all segments
    similarities = []
    for i, seg_embedding in enumerate(index["embeddings"]):
        similarity = cosine_similarity(query_embedding, seg_embedding)
        similarities.append((i, similarity))

    # Sort by similarity descending
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Return top_k results
    results = []
    for idx, score in similarities[:top_k]:
        seg = index["segments"][idx]
        results.append({
            "segment_index": seg["index"],
            "text": seg["text"],
            "speaker_tag": seg.get("speaker_tag"),
            "confidence": seg.get("confidence"),
            "similarity_score": round(score, 4),
        })

    return results


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    """
    import math

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def build_semantic_index(
    segments: List[TranscriptSegment],
    model: str = "text-embedding-3-large",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build a complete semantic index from transcript segments.

    Returns a serializable index structure for storage.
    """
    index = {
        "segments": [],
        "embeddings": [],
        "model": model,
        "total_segments": len(segments),
        "metadata": {
            "provider": "openai",
            "endpoint": "api.openai.com",
        },
    }

    embeddings = embed_segments(segments, model=model, api_key=api_key)

    for emb in embeddings:
        index["segments"].append({
            "index": emb["segment_index"],
            "text": emb["text"],
            "speaker_tag": emb["speaker_tag"],
            "confidence": emb["confidence"],
        })
        index["embeddings"].append(emb["embedding"])

    return index


if __name__ == "__main__":
    import sys

    print("Usage: Import transcript_embedding and use with transcription results.")
    print("Example:")
    print("  from transcript_embedding import build_semantic_index, search_similar_segments")
    print("  index = build_semantic_index(segments)")
    print("  results = search_similar_segments('What did they decide about the budget?', index)")
    print("  for r in results:")
    print("      print(f\"[{r['similarity_score']}] {r['text']}\")")
