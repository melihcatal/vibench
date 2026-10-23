import os
import numpy as np
from typing import List, Dict, Any, Optional
from openai import OpenAI
from fetch_recent_logs import fetch_recent_logs


def embed_log_message(
    text: str, model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Embed selected log messages for semantic retrieval using OpenAI Embeddings API.

    Args:
        text: Text to embed
        model: OpenAI embedding model to use

    Returns:
        Dictionary with embedding results
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=text, encoding_format="float"
        )

        embedding = response.data[0].embedding
        dimensions = len(embedding)

        result = {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "embedding_vector": embedding[:10],  # First 10 dimensions for preview
            "embedding_dimensions": dimensions,
            "model_used": model,
            "api_used": "OpenAI Embeddings API",
        }

        return result

    except Exception as e:
        print(f"Error creating embedding with OpenAI: {e}")
        return {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "error": str(e),
            "model_used": model,
            "api_used": "OpenAI Embeddings API",
        }


def embed_recent_logs(
    hours_back: int = 1,
    limit: int = 20,
    model: str = "text-embedding-3-small",
    min_text_length: int = 10,
) -> List[Dict[str, Any]]:
    """
    Embed recent log messages for semantic retrieval using OpenAI Embeddings API.

    Args:
        hours_back: Number of hours to look back
        limit: Maximum number of logs to embed
        model: OpenAI embedding model to use
        min_text_length: Minimum text length to embed

    Returns:
        List of embedding results with context
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    logs = fetch_recent_logs(hours_back=hours_back, limit=limit)

    client = OpenAI(api_key=api_key)
    results = []

    texts_to_embed = []
    log_contexts = []

    for log in logs:
        if not log.message or len(log.message.strip()) < min_text_length:
            continue

        texts_to_embed.append(log.message)
        log_contexts.append(
            {
                "timestamp": log.timestamp,
                "severity": log.severity,
                "component": log.labels.get("component", "unknown"),
                "trace_id": log.trace_id,
                "original_message": log.message,
            }
        )

    if not texts_to_embed:
        print("No log messages found to embed")
        return []

    try:
        response = client.embeddings.create(
            model=model, input=texts_to_embed, encoding_format="float"
        )

        for i, embedding_data in enumerate(response.data):
            if i < len(log_contexts):
                context = log_contexts[i]

                result = {
                    "timestamp": context["timestamp"].isoformat(),
                    "severity": context["severity"],
                    "component": context["component"],
                    "trace_id": context["trace_id"],
                    "original_message": context["original_message"][:150] + "..."
                    if len(context["original_message"]) > 150
                    else context["original_message"],
                    "embedding_dimensions": len(embedding_data.embedding),
                    "embedding_preview": embedding_data.embedding[
                        :5
                    ],  # First 5 dimensions
                    "model_used": model,
                    "api_used": "OpenAI Embeddings API",
                }

                results.append(result)

        print(f"Embedded {len(results)} log messages using OpenAI {model}")
        return results

    except Exception as e:
        print(f"Error embedding logs with OpenAI: {e}")
        return []


def semantic_search_logs(
    query: str,
    log_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = "text-embedding-3-small",
) -> List[Dict[str, Any]]:
    """
    Perform semantic search on embedded log messages using OpenAI Embeddings.

    Args:
        query: Search query
        log_embeddings: List of log embedding results
        top_k: Number of top results to return
        model: OpenAI embedding model to use

    Returns:
        List of search results with similarity scores
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = OpenAI(api_key=api_key)

    try:
        query_response = client.embeddings.create(
            model=model, input=query, encoding_format="float"
        )

        query_embedding = np.array(query_response.data[0].embedding)

        similarities = []

        for log in log_embeddings:
            if "embedding_vector" not in log or not log["embedding_vector"]:
                continue

            log_embedding = np.array(log["embedding_vector"])

            if len(log_embedding) != len(query_embedding):
                continue

            similarity = np.dot(query_embedding, log_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(log_embedding)
            )

            similarities.append({"log": log, "similarity": float(similarity)})

        similarities.sort(key=lambda x: x["similarity"], reverse=True)

        results = []
        for item in similarities[:top_k]:
            result = {
                "message": item["log"].get(
                    "text", item["log"].get("original_message", "N/A")
                ),
                "similarity_score": item["similarity"],
                "severity": item["log"].get("severity", "UNKNOWN"),
                "component": item["log"].get("component", "unknown"),
                "timestamp": item["log"].get("timestamp", "N/A"),
            }
            results.append(result)

        print(f"Semantic search completed using OpenAI {model}")
        print(f"Query: {query}")
        print(f"Found {len(results)} relevant logs")

        return results

    except Exception as e:
        print(f"Error performing semantic search: {e}")
        return []


def create_log_embedding_index(
    hours_back: int = 24, limit: int = 100, model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Create an embedding index of recent logs for semantic retrieval.

    Args:
        hours_back: Number of hours to look back
        limit: Maximum number of logs to include
        model: OpenAI embedding model to use

    Returns:
        Dictionary with embedding index
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    logs = fetch_recent_logs(hours_back=hours_back, limit=limit)

    client = OpenAI(api_key=api_key)

    texts_to_embed = []
    log_metadata = []

    for log in logs:
        if not log.message or len(log.message.strip()) < 10:
            continue

        texts_to_embed.append(log.message)
        log_metadata.append(
            {
                "timestamp": log.timestamp.isoformat(),
                "severity": log.severity,
                "component": log.labels.get("component", "unknown"),
                "trace_id": log.trace_id,
                "labels": log.labels,
            }
        )

    if not texts_to_embed:
        return {
            "index_size": 0,
            "model_used": model,
            "api_used": "OpenAI Embeddings API",
            "embeddings": [],
        }

    try:
        response = client.embeddings.create(
            model=model, input=texts_to_embed, encoding_format="float"
        )

        embeddings = []
        for i, embedding_data in enumerate(response.data):
            if i < len(log_metadata):
                embeddings.append(
                    {
                        "metadata": log_metadata[i],
                        "embedding": embedding_data.embedding,
                        "text_preview": texts_to_embed[i][:100],
                    }
                )

        index_info = {
            "index_size": len(embeddings),
            "model_used": model,
            "api_used": "OpenAI Embeddings API",
            "embedding_dimensions": len(embeddings[0]["embedding"])
            if embeddings
            else 0,
            "time_range_hours": hours_back,
            "embeddings": embeddings,
        }

        print(
            f"Created embedding index with {len(embeddings)} log entries using OpenAI {model}"
        )
        return index_info

    except Exception as e:
        print(f"Error creating embedding index: {e}")
        return {
            "index_size": 0,
            "model_used": model,
            "api_used": "OpenAI Embeddings API",
            "error": str(e),
        }


if __name__ == "__main__":
    test_messages = [
        "Database connection timeout after 30 seconds",
        "User authentication failed: invalid credentials",
        "High CPU usage detected on server node-01",
        "Payment processing completed successfully",
    ]

    for msg in test_messages:
        result = embed_log_message(msg, model="text-embedding-3-small")
        print(f"Message: {msg[:50]}...")
        print(f"  Model: {result.get('model_used', 'N/A')}")
        print(f"  Dimensions: {result.get('embedding_dimensions', 'N/A')}")
        print()
