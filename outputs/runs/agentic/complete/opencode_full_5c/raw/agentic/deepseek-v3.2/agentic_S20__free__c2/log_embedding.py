import os
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import faiss


def embed_log_messages(
    log_messages: List[str], model_name: str = "all-MiniLM-L6-v2", batch_size: int = 32
) -> Dict[str, Any]:
    """
    Embed selected log messages for semantic retrieval using Sentence Transformers.

    Args:
        log_messages: List of log message strings to embed
        model_name: Sentence Transformer model name
        batch_size: Batch size for embedding generation

    Returns:
        Dictionary with embeddings and metadata
    """
    if not log_messages:
        return {
            "summary": "No messages to embed",
            "embedding_count": 0,
            "model_used": model_name,
        }

    try:
        # Load the Sentence Transformer model
        model = SentenceTransformer(model_name)

        # Generate embeddings
        embeddings = model.encode(
            log_messages,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
        )

        # Convert to list for JSON serialization
        embeddings_list = embeddings.tolist()

        # Calculate embedding statistics
        embedding_dim = embeddings.shape[1]
        norm_stats = {
            "min_norm": float(np.min(np.linalg.norm(embeddings, axis=1))),
            "max_norm": float(np.max(np.linalg.norm(embeddings, axis=1))),
            "mean_norm": float(np.mean(np.linalg.norm(embeddings, axis=1))),
            "std_norm": float(np.std(np.linalg.norm(embeddings, axis=1))),
        }

        summary = {
            "total_messages": len(log_messages),
            "embedding_dimensions": embedding_dim,
            "model_used": model_name,
            "embedding_shape": embeddings.shape,
            "norm_statistics": norm_stats,
            "embedding_service": "Sentence Transformers",
            "model_details": {
                "provider": "Hugging Face",
                "model_family": "sentence-transformers",
                "vector_size": embedding_dim,
            },
        }

        # Create result entries
        entries = []
        for i, (message, embedding) in enumerate(zip(log_messages, embeddings_list)):
            entries.append(
                {
                    "message_index": i,
                    "message_preview": message[:100]
                    + ("..." if len(message) > 100 else ""),
                    "embedding": embedding,
                    "embedding_norm": float(np.linalg.norm(embeddings[i])),
                    "message_length": len(message),
                }
            )

        return {
            "summary": summary,
            "embeddings": entries,
            "raw_embeddings_array": embeddings_list,  # For downstream processing
        }

    except Exception as e:
        return {
            "summary": {
                "total_messages": len(log_messages),
                "embedding_dimensions": 0,
                "model_used": model_name,
                "error": str(e),
                "embedding_service": "Failed",
            },
            "embeddings": [],
            "error": str(e),
        }


def build_semantic_index(
    log_entries: List[Dict[str, Any]],
    embedding_field: str = "message",
    index_type: str = "flat",
) -> Dict[str, Any]:
    """
    Build a FAISS index for semantic search over log entries.

    Args:
        log_entries: List of log entry dictionaries
        embedding_field: Field to use for embedding generation
        index_type: FAISS index type ('flat', 'ivf', 'hnsw')

    Returns:
        Dictionary with index and metadata
    """
    # Extract messages for embedding
    messages = []
    valid_indices = []

    for i, entry in enumerate(log_entries):
        if embedding_field in entry and isinstance(entry[embedding_field], str):
            messages.append(entry[embedding_field])
            valid_indices.append(i)

    if not messages:
        return {
            "summary": f"No valid '{embedding_field}' fields found in log entries",
            "index_size": 0,
            "valid_entries": 0,
        }

    # Generate embeddings
    embedding_result = embed_log_messages(messages)

    if "error" in embedding_result:
        return {
            "summary": f"Failed to generate embeddings: {embedding_result.get('error', 'Unknown error')}",
            "index_size": 0,
            "valid_entries": len(valid_indices),
        }

    embeddings = np.array(
        [entry["embedding"] for entry in embedding_result["embeddings"]]
    )
    embedding_dim = embeddings.shape[1]

    # Create FAISS index
    if index_type == "flat":
        index = faiss.IndexFlatL2(embedding_dim)
    elif index_type == "ivf":
        # IVF index with 4 clusters
        quantizer = faiss.IndexFlatL2(embedding_dim)
        index = faiss.IndexIVFFlat(quantizer, embedding_dim, min(4, len(messages)))
        if len(messages) >= 4:
            index.train(embeddings)
    elif index_type == "hnsw":
        # HNSW index for approximate nearest neighbors
        index = faiss.IndexHNSWFlat(embedding_dim, 32)
    else:
        index = faiss.IndexFlatL2(embedding_dim)

    # Add embeddings to index
    index.add(embeddings)

    # Create metadata for each indexed entry
    metadata = []
    for idx, entry_idx in enumerate(valid_indices):
        metadata.append(
            {
                "log_entry_index": entry_idx,
                "original_entry": log_entries[entry_idx],
                "embedding_index": idx,
                "message": messages[idx],
            }
        )

    summary = {
        "total_log_entries": len(log_entries),
        "indexed_entries": len(valid_indices),
        "embedding_dimensions": embedding_dim,
        "index_type": index_type,
        "faiss_index_size": index.ntotal,
        "embedding_model": embedding_result["summary"]["model_used"],
        "index_built_at": "2024-01-15T10:00:00Z",  # Would use datetime.utcnow() in production
    }

    return {
        "summary": summary,
        "index": index,
        "metadata": metadata,
        "embeddings": embeddings,
        "valid_indices": valid_indices,
        "embedding_result": embedding_result["summary"],
    }


def semantic_search(
    index_result: Dict[str, Any],
    query: str,
    k: int = 5,
    threshold: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Perform semantic search over indexed log entries.

    Args:
        index_result: Result from build_semantic_index
        query: Search query string
        k: Number of results to return
        threshold: Optional similarity threshold

    Returns:
        Dictionary with search results
    """
    if "index" not in index_result:
        return {"error": "No index available for search", "query": query, "results": []}

    index = index_result["index"]
    metadata = index_result.get("metadata", [])
    embeddings = index_result.get("embeddings")

    if index.ntotal == 0:
        return {"summary": "Index is empty", "query": query, "results": []}

    # Generate embedding for query
    query_embedding_result = embed_log_messages([query])
    if "error" in query_embedding_result or not query_embedding_result["embeddings"]:
        return {"error": "Failed to embed query", "query": query, "results": []}

    query_embedding = np.array([query_embedding_result["embeddings"][0]["embedding"]])

    # Search the index
    k = min(k, index.ntotal)
    distances, indices = index.search(query_embedding, k)

    # Prepare results
    results = []
    for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
        if idx < 0 or idx >= len(metadata):  # Invalid index
            continue

        if threshold is not None and distance > threshold:
            continue

        meta = metadata[idx]
        result = {
            "rank": i + 1,
            "distance": float(distance),
            "similarity_score": float(
                1.0 / (1.0 + distance)
            ),  # Convert distance to similarity
            "log_entry_index": meta["log_entry_index"],
            "message": meta["message"],
            "original_entry": meta["original_entry"],
        }

        # Add additional context if available
        entry = meta["original_entry"]
        for field in ["timestamp", "severity", "service", "correlation_id"]:
            if field in entry:
                result[field] = entry[field]

        results.append(result)

    # Sort by similarity (highest first)
    results.sort(key=lambda x: x["similarity_score"], reverse=True)

    summary = {
        "query": query,
        "total_results": len(results),
        "k_requested": k,
        "distance_threshold": threshold,
        "query_embedding_dim": query_embedding.shape[1],
        "index_size": index.ntotal,
    }

    if results:
        summary["min_distance"] = min(r["distance"] for r in results)
        summary["max_similarity"] = max(r["similarity_score"] for r in results)
        summary["avg_similarity"] = sum(r["similarity_score"] for r in results) / len(
            results
        )

    return {
        "summary": summary,
        "results": results,
        "query_embedding": query_embedding_result["embeddings"][0]
        if query_embedding_result["embeddings"]
        else None,
    }


def find_similar_logs(
    log_entries: List[Dict[str, Any]], reference_index: int, k: int = 5
) -> Dict[str, Any]:
    """
    Find logs similar to a reference log entry.

    Args:
        log_entries: List of log entry dictionaries
        reference_index: Index of reference log entry
        k: Number of similar logs to find

    Returns:
        Dictionary with similar logs
    """
    if reference_index < 0 or reference_index >= len(log_entries):
        return {
            "error": f"Invalid reference index: {reference_index}",
            "valid_range": f"0-{len(log_entries) - 1}",
        }

    reference_entry = log_entries[reference_index]
    if "message" not in reference_entry:
        return {
            "error": "Reference log entry has no 'message' field",
            "reference_index": reference_index,
        }

    # Build index for all logs
    index_result = build_semantic_index(log_entries)

    if "index" not in index_result:
        return {
            "error": "Failed to build semantic index",
            "reference_index": reference_index,
        }

    # Find the reference entry in the index metadata
    reference_meta_idx = None
    for i, meta in enumerate(index_result.get("metadata", [])):
        if meta["log_entry_index"] == reference_index:
            reference_meta_idx = i
            break

    if reference_meta_idx is None:
        return {
            "error": "Reference entry not found in index",
            "reference_index": reference_index,
        }

    # Get the reference embedding
    reference_embedding = index_result["embeddings"][
        reference_meta_idx : reference_meta_idx + 1
    ]

    # Search for similar logs (excluding the reference itself)
    index = index_result["index"]
    k = min(k + 1, index.ntotal)  # +1 to account for self-match

    distances, indices = index.search(reference_embedding, k)

    # Prepare results, skipping the reference itself
    similar_logs = []
    for distance, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(index_result["metadata"]):
            continue

        meta = index_result["metadata"][idx]
        if meta["log_entry_index"] == reference_index:
            continue  # Skip the reference itself

        similarity = 1.0 / (1.0 + distance)

        similar_logs.append(
            {
                "log_entry_index": meta["log_entry_index"],
                "distance": float(distance),
                "similarity_score": float(similarity),
                "message": meta["message"],
                "original_entry": meta["original_entry"],
            }
        )

        if len(similar_logs) >= k - 1:  # -1 because we skipped reference
            break

    # Sort by similarity
    similar_logs.sort(key=lambda x: x["similarity_score"], reverse=True)

    return {
        "reference_entry": reference_entry,
        "reference_index": reference_index,
        "similar_logs_found": len(similar_logs),
        "similar_logs": similar_logs,
        "index_statistics": index_result["summary"],
    }


if __name__ == "__main__":
    # Example usage
    test_logs = [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "severity": "ERROR",
            "message": "Database connection timeout after 30 seconds",
            "service": "user-service",
        },
        {
            "timestamp": "2024-01-15T10:31:00Z",
            "severity": "ERROR",
            "message": "Failed to connect to PostgreSQL database",
            "service": "user-service",
        },
        {
            "timestamp": "2024-01-15T10:32:00Z",
            "severity": "INFO",
            "message": "User authentication successful",
            "service": "auth-service",
        },
        {
            "timestamp": "2024-01-15T10:33:00Z",
            "severity": "WARNING",
            "message": "High memory usage detected in container",
            "service": "monitoring-service",
        },
        {
            "timestamp": "2024-01-15T10:34:00Z",
            "severity": "ERROR",
            "message": "Connection to database server timed out",
            "service": "payment-service",
        },
    ]

    # Test embedding generation
    messages = [log["message"] for log in test_logs]
    embedding_result = embed_log_messages(messages)
    print(f"Generated {len(embedding_result['embeddings'])} embeddings")
    print(
        f"Embedding dimensions: {embedding_result['summary']['embedding_dimensions']}"
    )

    # Test index building
    index_result = build_semantic_index(test_logs)
    print(f"\nBuilt index with {index_result['summary']['indexed_entries']} entries")

    # Test semantic search
    search_result = semantic_search(index_result, "database connection problems", k=3)
    print(
        f"\nSearch for 'database connection problems': {len(search_result['results'])} results"
    )
    for result in search_result["results"]:
        print(f"  Similarity: {result['similarity_score']:.3f} - {result['message']}")

    # Test finding similar logs
    similar_result = find_similar_logs(test_logs, reference_index=0, k=2)
    print(f"\nLogs similar to index 0: {similar_result['similar_logs_found']} found")
    for log in similar_result["similar_logs"]:
        print(f"  Similarity: {log['similarity_score']:.3f} - {log['message']}")
