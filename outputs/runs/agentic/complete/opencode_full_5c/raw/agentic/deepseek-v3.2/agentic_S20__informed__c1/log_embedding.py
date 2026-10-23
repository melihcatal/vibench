import os
import json
from typing import List, Dict, Any, Optional
import numpy as np
from openai import OpenAI


def embed_log_message(
    log_message: str, model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """Embed selected log messages for semantic retrieval using OpenAI Embeddings API."""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    try:
        # Call OpenAI Embeddings API
        response = client.embeddings.create(
            model=model, input=log_message, encoding_format="float"
        )

        # Extract embedding vector
        embedding_vector = response.data[0].embedding
        embedding_dim = len(embedding_vector)

        # Calculate basic statistics
        vector_np = np.array(embedding_vector)
        stats = {
            "dimensions": embedding_dim,
            "mean": float(np.mean(vector_np)),
            "std": float(np.std(vector_np)),
            "min": float(np.min(vector_np)),
            "max": float(np.max(vector_np)),
            "norm": float(np.linalg.norm(vector_np)),
        }

        return {
            "embedding": {
                "vector": embedding_vector,
                "dimensions": embedding_dim,
                "statistics": stats,
            },
            "metadata": {
                "model": model,
                "provider": "OpenAI",
                "message_length": len(log_message),
                "tokens_used": response.usage.total_tokens,
                "embedding_id": response.data[0].embedding_id,
            },
        }

    except Exception as e:
        return {
            "embedding": {"vector": None, "error": str(e)},
            "metadata": {
                "model": model,
                "provider": "OpenAI",
                "error": True,
                "error_message": str(e),
            },
        }


def embed_logs_batch(
    log_messages: List[str], model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """Embed multiple log messages in batch."""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    try:
        # Batch embedding call
        response = client.embeddings.create(
            model=model, input=log_messages, encoding_format="float"
        )

        embeddings = []
        total_tokens = 0

        for i, embedding_data in enumerate(response.data):
            embedding_vector = embedding_data.embedding
            vector_np = np.array(embedding_vector)

            stats = {
                "dimensions": len(embedding_vector),
                "mean": float(np.mean(vector_np)),
                "std": float(np.std(vector_np)),
                "norm": float(np.linalg.norm(vector_np)),
            }

            embeddings.append(
                {
                    "index": i,
                    "message_preview": log_messages[i][:100]
                    + ("..." if len(log_messages[i]) > 100 else ""),
                    "embedding_vector": embedding_vector,
                    "statistics": stats,
                    "embedding_id": embedding_data.embedding_id,
                }
            )

            total_tokens += (
                embedding_data.usage.total_tokens
                if hasattr(embedding_data, "usage")
                else 0
            )

        # Calculate similarity matrix
        similarity_matrix = None
        if len(embeddings) > 1:
            vectors = [np.array(emb["embedding_vector"]) for emb in embeddings]
            similarity_matrix = calculate_cosine_similarity_matrix(vectors)

        return {
            "batch_embeddings": {
                "total_embeddings": len(embeddings),
                "model": model,
                "dimensions": len(embeddings[0]["embedding_vector"])
                if embeddings
                else 0,
                "total_tokens": total_tokens,
            },
            "embeddings": embeddings,
            "similarity_analysis": similarity_matrix,
            "metadata": {
                "provider": "OpenAI",
                "model": model,
                "batch_size": len(log_messages),
            },
        }

    except Exception as e:
        return {
            "batch_embeddings": {"total_embeddings": 0, "error": str(e)},
            "embeddings": [],
            "similarity_analysis": None,
            "metadata": {
                "provider": "OpenAI",
                "model": model,
                "error": True,
                "error_message": str(e),
            },
        }


def calculate_cosine_similarity(
    embedding1: List[float], embedding2: List[float]
) -> float:
    """Calculate cosine similarity between two embedding vectors."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def calculate_cosine_similarity_matrix(embeddings: List[np.ndarray]) -> Dict[str, Any]:
    """Calculate cosine similarity matrix for multiple embeddings."""
    n = len(embeddings)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 1.0
            elif j > i:
                similarity = calculate_cosine_similarity(embeddings[i], embeddings[j])
                matrix[i][j] = similarity
                matrix[j][i] = similarity

    # Find most similar pairs
    most_similar_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            similarity = matrix[i][j]
            most_similar_pairs.append({"pair": (i, j), "similarity": similarity})

    # Sort by similarity
    most_similar_pairs.sort(key=lambda x: x["similarity"], reverse=True)

    # Calculate statistics
    similarities = matrix[np.triu_indices(n, k=1)]  # Upper triangle without diagonal
    stats = {
        "mean_similarity": float(np.mean(similarities)),
        "std_similarity": float(np.std(similarities)),
        "min_similarity": float(np.min(similarities)),
        "max_similarity": float(np.max(similarities)),
        "total_pairs": len(similarities),
    }

    return {
        "matrix": matrix.tolist(),
        "statistics": stats,
        "most_similar_pairs": most_similar_pairs[:10],  # Top 10 most similar pairs
    }


def search_similar_logs(
    query: str,
    log_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = "text-embedding-3-small",
) -> Dict[str, Any]:
    """Search for logs similar to a query using embeddings."""

    # Embed the query
    query_embedding_result = embed_log_message(query, model)

    if query_embedding_result["embedding"].get("vector") is None:
        return {
            "search_results": [],
            "error": query_embedding_result["embedding"].get("error"),
            "metadata": {"query": query, "top_k": top_k},
        }

    query_vector = np.array(query_embedding_result["embedding"]["vector"])

    # Calculate similarities
    similarities = []
    for i, log_emb in enumerate(log_embeddings):
        if "embedding_vector" in log_emb:
            log_vector = np.array(log_emb["embedding_vector"])
            similarity = calculate_cosine_similarity(query_vector, log_vector)

            similarities.append(
                {
                    "index": i,
                    "similarity": similarity,
                    "log_data": log_emb.get("log_data", {}),
                    "message": log_emb.get("message_preview", f"Log {i}"),
                }
            )

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    # Take top_k results
    top_results = similarities[:top_k]

    return {
        "search_results": top_results,
        "query_embedding": query_embedding_result,
        "metadata": {
            "query": query,
            "total_logs_searched": len(log_embeddings),
            "top_k": top_k,
            "model": model,
            "provider": "OpenAI",
        },
    }


if __name__ == "__main__":
    # Example usage
    test_message = "Error: Database connection timeout after 30 seconds"

    result = embed_log_message(test_message)
    print("Embedding Result:")
    print(f"Dimensions: {result['embedding']['dimensions']}")
    print(f"Vector preview: {result['embedding']['vector'][:5]}...")
    print(f"Statistics: {json.dumps(result['embedding']['statistics'], indent=2)}")

    # Batch example
    test_messages = [
        "Error: Database connection failed",
        "Warning: High memory usage detected",
        "Info: User login successful",
        "Error: API request timeout",
    ]

    batch_result = embed_logs_batch(test_messages)
    print(
        f"\nBatch Embeddings: {batch_result['batch_embeddings']['total_embeddings']} embeddings created"
    )

    if batch_result.get("similarity_analysis"):
        print(
            f"Mean similarity: {batch_result['similarity_analysis']['statistics']['mean_similarity']:.3f}"
        )

        # Search example
        search_query = "database error timeout"
        search_results = search_similar_logs(
            query=search_query, log_embeddings=batch_result["embeddings"], top_k=3
        )

        print(f"\nSearch results for '{search_query}':")
        for i, result in enumerate(search_results["search_results"]):
            print(
                f"{i + 1}. Similarity: {result['similarity']:.3f} - {result['message']}"
            )
