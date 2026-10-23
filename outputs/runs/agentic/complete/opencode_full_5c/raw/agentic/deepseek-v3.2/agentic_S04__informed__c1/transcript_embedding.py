import openai
import os
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EmbeddingResult:
    """Result of embedding generation."""

    text: str
    embedding: List[float]
    model: str
    token_count: int


def embed_transcript_segments(
    segments: List[Dict[str, Any]], model: str = "text-embedding-3-small"
) -> List[EmbeddingResult]:
    """
    Embed transcript segments for semantic retrieval using OpenAI Embeddings API.

    Args:
        segments: List of transcript segments with 'text' field
        model: OpenAI embedding model to use

    Returns:
        List of embedding results
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    texts = [segment.get("text", "") for segment in segments]

    if not any(texts):
        return []

    try:
        response = client.embeddings.create(
            model=model, input=texts, encoding_format="float"
        )

        results = []
        for i, data in enumerate(response.data):
            segment = segments[i] if i < len(segments) else {}
            results.append(
                EmbeddingResult(
                    text=texts[i],
                    embedding=data.embedding,
                    model=model,
                    token_count=data.usage.total_tokens
                    if hasattr(data, "usage")
                    else 0,
                )
            )

        return results

    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []


def embed_transcript_text(
    text: str, model: str = "text-embedding-3-small"
) -> Optional[EmbeddingResult]:
    """
    Embed a single transcript text.

    Args:
        text: Text to embed
        model: OpenAI embedding model to use

    Returns:
        Embedding result or None if error
    """
    if not text.strip():
        return None

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.embeddings.create(
            model=model, input=[text], encoding_format="float"
        )

        data = response.data[0]
        return EmbeddingResult(
            text=text,
            embedding=data.embedding,
            model=model,
            token_count=data.usage.total_tokens if hasattr(data, "usage") else 0,
        )

    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


def create_semantic_index(
    transcript_data: Dict[str, Any], segment_duration: float = 30.0
) -> Dict[str, Any]:
    """
    Create a semantic index of transcript segments with embeddings.

    Args:
        transcript_data: Transcript data from poll_transcription_job
        segment_duration: Duration for segmenting transcript

    Returns:
        Semantic index with embeddings
    """
    from timestamped_transcript import get_segmented_transcript

    segments = get_segmented_transcript(
        transcript_data.get("job_name", ""), segment_duration=segment_duration
    )

    if not segments:
        segments = [{"text": transcript_data.get("transcript", "")}]

    embeddings = embed_transcript_segments(segments)

    index_entries = []
    for i, (segment, embedding_result) in enumerate(zip(segments, embeddings)):
        entry = {
            "segment_id": i,
            "start_time": segment.get("start_time"),
            "end_time": segment.get("end_time"),
            "text": segment.get("text", ""),
            "embedding": embedding_result.embedding if embedding_result else [],
            "embedding_model": embedding_result.model if embedding_result else None,
            "word_count": segment.get("word_count", 0),
            "speaker": segment.get("speaker"),
        }
        index_entries.append(entry)

    return {
        "transcript_id": transcript_data.get("job_name", "unknown"),
        "total_segments": len(segments),
        "embedding_model": embeddings[0].model if embeddings else None,
        "segments": index_entries,
        "metadata": {
            "source": "Amazon Transcribe",
            "embedding_provider": "OpenAI",
            "segment_duration": segment_duration,
        },
    }


def semantic_search(
    index: Dict[str, Any], query: str, top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform semantic search on transcript index.

    Args:
        index: Semantic index from create_semantic_index
        query: Search query
        top_k: Number of top results to return

    Returns:
        Top matching segments with similarity scores
    """
    query_embedding_result = embed_transcript_text(query)
    if not query_embedding_result:
        return []

    query_embedding = np.array(query_embedding_result.embedding)

    similarities = []

    for segment in index["segments"]:
        if not segment.get("embedding"):
            continue

        segment_embedding = np.array(segment["embedding"])

        similarity = cosine_similarity(query_embedding, segment_embedding)

        similarities.append({"segment": segment, "similarity": similarity})

    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.

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


def find_similar_segments(
    transcript_data: Dict[str, Any], reference_text: str, top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Find segments similar to reference text within a transcript.

    Args:
        transcript_data: Transcript data
        reference_text: Reference text to compare against
        top_k: Number of similar segments to find

    Returns:
        Similar segments with similarity scores
    """
    index = create_semantic_index(transcript_data)
    return semantic_search(index, reference_text, top_k)


def cluster_transcript_segments(
    transcript_data: Dict[str, Any], n_clusters: int = 5
) -> Dict[str, Any]:
    """
    Cluster transcript segments by semantic similarity.

    Args:
        transcript_data: Transcript data
        n_clusters: Number of clusters to create

    Returns:
        Clustering results
    """
    from sklearn.cluster import KMeans

    index = create_semantic_index(transcript_data)

    embeddings = []
    valid_segments = []

    for segment in index["segments"]:
        if segment.get("embedding"):
            embeddings.append(segment["embedding"])
            valid_segments.append(segment)

    if len(embeddings) < n_clusters:
        n_clusters = len(embeddings)

    if not embeddings:
        return {"clusters": [], "error": "No embeddings available"}

    embeddings_array = np.array(embeddings)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(embeddings_array)

    clusters = []
    for cluster_id in range(n_clusters):
        cluster_segments = [
            valid_segments[i]
            for i in range(len(valid_segments))
            if cluster_labels[i] == cluster_id
        ]

        cluster_texts = [seg["text"] for seg in cluster_segments]
        cluster_center = kmeans.cluster_centers_[cluster_id]

        clusters.append(
            {
                "cluster_id": cluster_id,
                "segment_count": len(cluster_segments),
                "segments": cluster_segments,
                "sample_texts": cluster_texts[:3],
                "center_embedding": cluster_center.tolist(),
            }
        )

    return {
        "transcript_id": transcript_data.get("job_name", "unknown"),
        "n_clusters": n_clusters,
        "total_segments": len(valid_segments),
        "clusters": clusters,
        "cluster_labels": cluster_labels.tolist(),
    }


def generate_transcript_embeddings_package(
    transcript_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate a complete embeddings package for a transcript.

    Args:
        transcript_data: Transcript data

    Returns:
        Complete embeddings package
    """
    index = create_semantic_index(transcript_data)

    summary_embedding = embed_transcript_text(transcript_data.get("transcript", ""))

    clusters = cluster_transcript_segments(transcript_data, n_clusters=5)

    return {
        "transcript_id": transcript_data.get("job_name", "unknown"),
        "embeddings_index": index,
        "summary_embedding": summary_embedding.embedding if summary_embedding else None,
        "summary_embedding_model": summary_embedding.model
        if summary_embedding
        else None,
        "clustering": clusters,
        "embedding_metadata": {
            "provider": "OpenAI",
            "primary_model": "text-embedding-3-small",
            "vector_dimension": len(index["segments"][0]["embedding"])
            if index["segments"] and index["segments"][0]["embedding"]
            else 0,
            "total_embeddings": len(index["segments"]),
        },
    }
