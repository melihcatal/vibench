"""
Embed transcript segments for semantic retrieval.
Provider: OpenAI Embeddings API (api.openai.com)
SDK: openai Python client with text-embedding-3-large model.
"""

import logging
import os
from typing import List, Dict, Any, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_HOST = "api.openai.com"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSIONS = 3072


def create_openai_client() -> OpenAI:
    """
    Create an OpenAI client for embeddings API calls.
    
    Provider: OpenAI (api.openai.com)
    SDK: openai Python package
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    client = OpenAI(api_key=api_key)
    logger.info(f"Initialized OpenAI client for {OPENAI_API_HOST}")
    return client


def embed_text_segment(
    text: str,
    model: str = EMBEDDING_MODEL,
    dimensions: int = EMBEDDING_DIMENSIONS,
) -> Dict[str, Any]:
    """
    Generate an embedding vector for a single text segment.
    
    Provider: OpenAI api.openai.com
    Model: text-embedding-3-large for high-dimensional semantic embeddings.
    
    Args:
        text: Text segment to embed
        model: OpenAI embedding model identifier
        dimensions: Output embedding dimensions
        
    Returns:
        Dict containing the embedding vector and metadata
    """
    client = create_openai_client()
    
    response = client.embeddings.create(
        input=text,
        model=model,
        dimensions=dimensions,
    )
    
    embedding_data = response.data[0]
    
    return {
        "text": text,
        "embedding": embedding_data.embedding,
        "model": model,
        "dimensions": len(embedding_data.embedding),
        "usage_tokens": response.usage.total_tokens,
        "provider": "openai",
        "api_host": OPENAI_API_HOST,
    }


def embed_transcript_segments(
    segments: List[str],
    model: str = EMBEDDING_MODEL,
    dimensions: int = EMBEDDING_DIMENSIONS,
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for multiple transcript segments.
    
    Provider: OpenAI api.openai.com with text-embedding-3-large model.
    Processes segments in batches for efficiency.
    
    Args:
        segments: List of text segments to embed
        model: OpenAI embedding model identifier
        dimensions: Output embedding dimensions
        batch_size: Number of segments per API call
        
    Returns:
        List of dicts with segment text and embedding vectors
    """
    client = create_openai_client()
    all_results = []
    
    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]
        
        response = client.embeddings.create(
            input=batch,
            model=model,
            dimensions=dimensions,
        )
        
        for j, embedding_data in enumerate(response.data):
            all_results.append({
                "index": i + j,
                "text": batch[j],
                "embedding": embedding_data.embedding,
                "model": model,
                "dimensions": len(embedding_data.embedding),
                "provider": "openai",
                "api_host": OPENAI_API_HOST,
            })
    
    return all_results


def embed_diarized_utterances(
    request_id: str,
) -> List[Dict[str, Any]]:
    """
    Embed utterances from a diarized transcript for semantic search.
    
    Uses OpenAI text-embedding-3-large at api.openai.com.
    Combines with diarized_transcript.py to get speaker utterances.
    """
    from diarized_transcript import get_diarized_transcript
    
    response = get_diarized_transcript(request_id)
    
    segments = []
    for utt in response.utterances:
        segments.append(f"Speaker {utt.speaker}: {utt.text}")
    
    if not segments:
        segments = [response.transcript_text]
    
    return embed_transcript_segments(segments)


def embed_for_semantic_retrieval(
    transcript_text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[Dict[str, Any]]:
    """
    Chunk transcript text and generate embeddings for semantic retrieval.
    
    Uses OpenAI text-embedding-3-large for creating searchable vectors.
    Provider: api.openai.com
    
    Args:
        transcript_text: Full transcript text
        chunk_size: Characters per chunk
        overlap: Character overlap between chunks
        
    Returns:
        List of embedded chunks with metadata
    """
    # Create overlapping chunks
    chunks = []
    start = 0
    while start < len(transcript_text):
        end = start + chunk_size
        chunk = transcript_text[start:end]
        
        # Try to break at sentence boundary
        if end < len(transcript_text):
            last_period = chunk.rfind(". ")
            if last_period > chunk_size // 2:
                chunk = chunk[:last_period + 1]
                end = start + last_period + 1
        
        chunks.append({
            "chunk_index": len(chunks),
            "text": chunk.strip(),
            "start_char": start,
            "end_char": end,
        })
        
        start = end - overlap if end < len(transcript_text) else end
    
    # Generate embeddings
    texts = [c["text"] for c in chunks]
    embeddings = embed_transcript_segments(texts)
    
    # Combine with chunk metadata
    for i, emb in enumerate(embeddings):
        emb["chunk_index"] = chunks[i]["chunk_index"]
        emb["start_char"] = chunks[i]["start_char"]
        emb["end_char"] = chunks[i]["end_char"]
    
    return embeddings


def cosine_similarity(
    vec_a: List[float],
    vec_b: List[float],
) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math
    
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)


def search_similar_segments(
    query: str,
    embedded_segments: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search for semantically similar segments using embeddings.
    
    Embeds the query with OpenAI text-embedding-3-large and finds
    the most similar segments by cosine similarity.
    """
    query_embedding = embed_text_segment(query)
    query_vec = query_embedding["embedding"]
    
    scored = []
    for segment in embedded_segments:
        similarity = cosine_similarity(query_vec, segment["embedding"])
        scored.append({
            **segment,
            "similarity_score": similarity,
        })
    
    # Sort by similarity descending
    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return scored[:top_k]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        result = embed_text_segment(text)
        print(f"Model: {result['model']}")
        print(f"Dimensions: {result['dimensions']}")
        print(f"Embedding preview: {result['embedding'][:5]}...")
    else:
        print("Usage: python transcript_embedding.py <text>")
