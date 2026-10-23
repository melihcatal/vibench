import os
from typing import List, Dict, Any
import numpy as np


def translation_memory_embedding(
    text_segments: List[str], metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Embed translated segments for translation-memory search.

    Args:
        text_segments: List of text segments to embed
        metadata: Optional metadata for the segments

    Returns:
        Dictionary with embeddings and metadata
    """
    # Use Cohere Embed API for embeddings
    import cohere

    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(api_key)

    # Generate embeddings using Cohere's embed model
    response = co.embed(
        texts=text_segments,
        model="embed-english-v3.0",  # Cohere's English embedding model
        input_type="search_document",
    )

    embeddings = response.embeddings

    # Prepare result structure
    result = {
        "provider": "cohere",
        "model": "embed-english-v3.0",
        "embeddings": embeddings,
        "text_segments": text_segments,
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "num_segments": len(text_segments),
        "metadata": metadata or {},
    }

    # Calculate some statistics
    if embeddings:
        embeddings_array = np.array(embeddings)
        result["statistics"] = {
            "mean_norm": float(np.mean(np.linalg.norm(embeddings_array, axis=1))),
            "std_norm": float(np.std(np.linalg.norm(embeddings_array, axis=1))),
            "shape": embeddings_array.shape,
        }

    return result


def search_translation_memory(
    query: str,
    embeddings: List[List[float]],
    text_segments: List[str],
    metadata_list: Optional[List[Dict[str, Any]]] = None,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search translation memory using embeddings.

    Args:
        query: Search query text
        embeddings: List of embedding vectors for stored segments
        text_segments: Corresponding text segments
        metadata_list: Optional metadata for each segment
        top_k: Number of top results to return

    Returns:
        List of search results with similarity scores
    """
    import cohere
    import numpy as np

    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(api_key)

    # Embed the query
    query_response = co.embed(
        texts=[query], model="embed-english-v3.0", input_type="search_query"
    )

    query_embedding = np.array(query_response.embeddings[0])
    stored_embeddings = np.array(embeddings)

    # Calculate cosine similarities
    query_norm = np.linalg.norm(query_embedding)
    stored_norms = np.linalg.norm(stored_embeddings, axis=1)

    # Avoid division by zero
    query_norm = max(query_norm, 1e-10)
    stored_norms = np.maximum(stored_norms, 1e-10)

    # Normalize embeddings
    query_embedding_norm = query_embedding / query_norm
    stored_embeddings_norm = stored_embeddings / stored_norms[:, np.newaxis]

    # Calculate cosine similarities
    similarities = np.dot(stored_embeddings_norm, query_embedding_norm)

    # Get top-k indices
    top_indices = np.argsort(similarities)[::-1][:top_k]

    # Prepare results
    results = []
    for idx in top_indices:
        result = {
            "text": text_segments[idx],
            "similarity": float(similarities[idx]),
            "rank": len(results) + 1,
            "index": int(idx),
        }

        if metadata_list and idx < len(metadata_list):
            result["metadata"] = metadata_list[idx]

        results.append(result)

    return results
