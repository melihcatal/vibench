import os
import numpy as np
from typing import List, Dict, Any
from speech_models import TranscriptionResult, TimestampedTranscript


def embed_transcript_segments(
    transcript: TranscriptionResult, model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Embed transcript segments for semantic retrieval using OpenAI Embeddings API.

    Args:
        transcript: TranscriptionResult object
        model: OpenAI embedding model to use

    Returns:
        Dictionary with embeddings and metadata
    """
    # Get OpenAI API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    import openai

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Prepare segments for embedding
    segments = []
    if hasattr(transcript, "segments") and transcript.segments:
        # Use timestamped segments
        for segment in transcript.segments:
            segments.append(
                {
                    "text": segment["text"],
                    "start_time": segment["start_time"],
                    "end_time": segment["end_time"],
                    "words": segment.get("words", []),
                }
            )
    else:
        # Split transcript into chunks
        import re

        sentences = re.split(r"(?<=[.!?])\s+", transcript.transcript)
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                segments.append(
                    {
                        "text": sentence.strip(),
                        "start_time": None,
                        "end_time": None,
                        "index": i,
                    }
                )

    # Batch embeddings (OpenAI supports up to 2048 inputs per batch)
    batch_size = 100
    all_embeddings = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i : i + batch_size]
        texts = [seg["text"] for seg in batch]

        try:
            response = client.embeddings.create(
                model=model, input=texts, encoding_format="float"
            )

            # Add embeddings to segments
            for j, embedding in enumerate(response.data):
                segments[i + j]["embedding"] = embedding.embedding
                segments[i + j]["embedding_model"] = model
                segments[i + j]["embedding_tokens"] = embedding.usage.prompt_tokens

            all_embeddings.extend([emb.embedding for emb in response.data])

        except openai.OpenAIError as e:
            print(f"Error generating embeddings for batch {i // batch_size}: {e}")
            # Add None embeddings for failed segments
            for j in range(len(batch)):
                segments[i + j]["embedding"] = None
                segments[i + j]["embedding_error"] = str(e)

    # Calculate centroid embedding for the entire transcript
    centroid = None
    valid_embeddings = [
        seg["embedding"] for seg in segments if seg.get("embedding") is not None
    ]

    if valid_embeddings:
        centroid = np.mean(valid_embeddings, axis=0).tolist()

    # Create embedding index for semantic search
    embedding_index = {
        "job_id": transcript.job_id,
        "model": model,
        "total_segments": len(segments),
        "segments_with_embeddings": len(valid_embeddings),
        "centroid_embedding": centroid,
        "segments": segments,
        "dimensions": len(centroid) if centroid else 0,
    }

    return embedding_index


def semantic_search(
    embedding_index: Dict[str, Any], query: str, top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform semantic search on embedded transcript segments.

    Args:
        embedding_index: Embedding index from embed_transcript_segments
        query: Search query
        top_k: Number of results to return

    Returns:
        List of matching segments with similarity scores
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    import openai
    from sklearn.metrics.pairwise import cosine_similarity

    client = openai.OpenAI(api_key=api_key)

    # Embed the query
    try:
        response = client.embeddings.create(
            model=embedding_index["model"], input=[query], encoding_format="float"
        )
        query_embedding = response.data[0].embedding

    except openai.OpenAIError as e:
        print(f"Error embedding query: {e}")
        return []

    # Calculate similarities
    results = []
    for segment in embedding_index["segments"]:
        if segment.get("embedding") is not None:
            # Calculate cosine similarity
            similarity = cosine_similarity([query_embedding], [segment["embedding"]])[
                0
            ][0]

            results.append(
                {
                    "text": segment["text"],
                    "start_time": segment.get("start_time"),
                    "end_time": segment.get("end_time"),
                    "similarity": float(similarity),
                    "segment_index": segment.get("index"),
                }
            )

    # Sort by similarity and return top_k
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


def cluster_transcript_segments(
    embedding_index: Dict[str, Any], n_clusters: int = 5
) -> Dict[str, Any]:
    """
    Cluster transcript segments by semantic similarity.

    Args:
        embedding_index: Embedding index from embed_transcript_segments
        n_clusters: Number of clusters to create

    Returns:
        Dictionary with clustering results
    """
    from sklearn.cluster import KMeans

    # Extract valid embeddings
    valid_segments = []
    valid_embeddings = []

    for segment in embedding_index["segments"]:
        if segment.get("embedding") is not None:
            valid_segments.append(segment)
            valid_embeddings.append(segment["embedding"])

    if not valid_embeddings:
        return {"error": "No valid embeddings available for clustering"}

    # Perform K-means clustering
    embeddings_array = np.array(valid_embeddings)
    kmeans = KMeans(n_clusters=min(n_clusters, len(valid_embeddings)), random_state=42)
    cluster_labels = kmeans.fit_predict(embeddings_array)

    # Organize segments by cluster
    clusters = {}
    for i, (segment, label) in enumerate(zip(valid_segments, cluster_labels)):
        if label not in clusters:
            clusters[label] = {
                "cluster_id": int(label),
                "centroid": kmeans.cluster_centers_[label].tolist(),
                "segments": [],
                "representative_texts": [],
            }

        clusters[label]["segments"].append(
            {
                "text": segment["text"],
                "start_time": segment.get("start_time"),
                "end_time": segment.get("end_time"),
            }
        )

    # Find representative segments for each cluster
    for cluster_id, cluster_data in clusters.items():
        # Use segments closest to centroid as representatives
        cluster_embeddings = embeddings_array[cluster_labels == cluster_id]
        centroid = kmeans.cluster_centers_[cluster_id]

        # Calculate distances to centroid
        distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
        closest_indices = np.argsort(distances)[:3]  # Top 3 closest

        # Get corresponding segments
        cluster_segments = [
            s for s, l in zip(valid_segments, cluster_labels) if l == cluster_id
        ]
        representative_texts = []

        for idx in closest_indices:
            if idx < len(cluster_segments):
                representative_texts.append(cluster_segments[idx]["text"][:200] + "...")

        cluster_data["representative_texts"] = representative_texts
        cluster_data["size"] = len(cluster_data["segments"])

    return {
        "job_id": embedding_index["job_id"],
        "n_clusters": len(clusters),
        "clusters": list(clusters.values()),
        "total_segments_clustered": len(valid_segments),
        "clustering_algorithm": "KMeans",
    }


if __name__ == "__main__":
    # Example usage
    import sys

    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        sys.exit(1)

    if len(sys.argv) > 1:
        # Create a mock transcript for testing
        mock_transcript = TranscriptionResult(
            job_id="test-job-123", transcript=sys.argv[1], language_code="en-US"
        )

        # Add some segments for testing
        mock_transcript.segments = [
            {
                "text": "First segment about machine learning.",
                "start_time": 0,
                "end_time": 5,
            },
            {
                "text": "Second segment about natural language processing.",
                "start_time": 5,
                "end_time": 10,
            },
            {
                "text": "Third segment about artificial intelligence.",
                "start_time": 10,
                "end_time": 15,
            },
        ]

        embedding_index = embed_transcript_segments(mock_transcript)
        print(
            f"Generated embeddings for {embedding_index['segments_with_embeddings']} segments"
        )

        # Test semantic search
        if len(sys.argv) > 2:
            query = sys.argv[2]
            results = semantic_search(embedding_index, query)
            print(f"\nSemantic search results for '{query}':")
            for result in results:
                print(
                    f"  Similarity: {result['similarity']:.3f} - {result['text'][:100]}..."
                )
    else:
        print("Usage: python transcript_embedding.py <transcript_text> [search_query]")
        print(
            "Example: python transcript_embedding.py 'Machine learning is...' 'artificial intelligence'"
        )
