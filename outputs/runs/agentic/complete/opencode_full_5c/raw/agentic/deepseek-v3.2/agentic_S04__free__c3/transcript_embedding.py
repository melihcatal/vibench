import os
import numpy as np
from typing import List, Dict, Any
from openai import OpenAI
from speech_models import NormalizedTranscript, TranscriptSegment


def transcript_embedding(
    transcript: NormalizedTranscript, embedding_model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Embed transcript segments for semantic retrieval using OpenAI Embeddings API.

    Args:
        transcript: Normalized transcript to embed
        embedding_model: OpenAI embedding model to use

    Returns:
        Dictionary with embeddings and metadata
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=openai_api_key)

    segments_for_embedding = prepare_segments_for_embedding(transcript)
    embeddings = []

    try:
        response = client.embeddings.create(
            model=embedding_model, input=segments_for_embedding, encoding_format="float"
        )

        for i, data in enumerate(response.data):
            embeddings.append(
                {
                    "segment_index": i,
                    "text": segments_for_embedding[i],
                    "embedding": data.embedding,
                    "token_count": data.usage.total_tokens
                    if hasattr(data, "usage")
                    else 0,
                }
            )

    except Exception as e:
        raise Exception(f"OpenAI Embeddings API error: {e}")

    return {
        "model": embedding_model,
        "embeddings": embeddings,
        "segment_count": len(embeddings),
        "embedding_dimension": len(embeddings[0]["embedding"]) if embeddings else 0,
        "transcript_metadata": transcript.metadata,
    }


def prepare_segments_for_embedding(
    transcript: NormalizedTranscript, max_segment_length: int = 500
) -> List[str]:
    """
    Prepare transcript segments for embedding.

    Args:
        transcript: Normalized transcript
        max_segment_length: Maximum characters per segment

    Returns:
        List of text segments ready for embedding
    """
    if not transcript.segments:
        chunks = split_text_into_chunks(transcript.text, max_segment_length)
        return chunks

    segments = []
    current_segment = ""
    current_start_time = None

    for seg in transcript.segments:
        segment_text = seg.text

        if len(current_segment) + len(segment_text) + 1 <= max_segment_length:
            if current_segment:
                current_segment += " " + segment_text
            else:
                current_segment = segment_text
                current_start_time = seg.start_time
        else:
            if current_segment:
                segments.append(current_segment)
            current_segment = segment_text
            current_start_time = seg.start_time

    if current_segment:
        segments.append(current_segment)

    return segments


def split_text_into_chunks(text: str, max_chars: int) -> List[str]:
    """
    Split text into chunks for embedding.

    Args:
        text: Text to split
        max_chars: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    sentences = text.split(". ")
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if sentence[-1] != ".":
            sentence += "."

        if len(current_chunk) + len(sentence) + 2 <= max_chars:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def semantic_search(
    query: str, embeddings_data: Dict[str, Any], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform semantic search on embedded transcript segments.

    Args:
        query: Search query
        embeddings_data: Embeddings data from transcript_embedding
        top_k: Number of top results to return

    Returns:
        List of search results with similarity scores
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=openai_api_key)

    try:
        query_response = client.embeddings.create(
            model=embeddings_data["model"], input=query, encoding_format="float"
        )
        query_embedding = query_response.data[0].embedding

    except Exception as e:
        raise Exception(f"OpenAI Embeddings API error for query: {e}")

    results = []
    query_vec = np.array(query_embedding)

    for emb_data in embeddings_data["embeddings"]:
        segment_vec = np.array(emb_data["embedding"])
        similarity = cosine_similarity(query_vec, segment_vec)

        results.append(
            {
                "segment_index": emb_data["segment_index"],
                "text": emb_data["text"],
                "similarity": similarity,
                "token_count": emb_data.get("token_count", 0),
            }
        )

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)
