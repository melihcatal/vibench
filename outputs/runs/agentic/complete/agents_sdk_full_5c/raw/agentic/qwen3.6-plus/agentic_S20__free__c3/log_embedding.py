"""
[LATER-STEP] Embeds selected log messages for semantic retrieval.

Uses the OpenAI Embeddings API (api.openai.com) with the text-embedding-3-small
model to create vector embeddings of log messages, enabling semantic search
and similarity-based log clustering.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Create an OpenAI client configured from environment variables.

    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)
    return client


def embed_log_message(
    message: str,
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
) -> Dict[str, Any]:
    """
    Generate an embedding vector for a single log message.

    Uses the OpenAI text-embedding-3-small model (1536 dimensions) to create
    a dense vector representation suitable for semantic similarity search.

    Args:
        message: The log message text to embed.
        client: Optional pre-configured OpenAI client.
        model: The OpenAI embedding model to use.

    Returns:
        Dictionary with the original text, embedding vector, model used,
        and dimension count.
    """
    if client is None:
        client = get_openai_client()

    response = client.embeddings.create(
        model=model,
        input=message,
    )

    embedding = response.data[0].embedding
    return {
        "text": message,
        "embedding": embedding,
        "model": model,
        "dimensions": len(embedding),
    }


def embed_log_messages(
    messages: List[str],
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
    batch_size: int = 500,
) -> List[Dict[str, Any]]:
    """
    Generate embedding vectors for multiple log messages.

    Processes messages in batches respecting OpenAI API input limits.

    Args:
        messages: List of log messages to embed.
        client: Optional pre-configured OpenAI client.
        model: The OpenAI embedding model to use.
        batch_size: Number of messages per batch (max 500 for text-embedding-3-small).

    Returns:
        List of embedding results, one per message.
    """
    if client is None:
        client = get_openai_client()

    all_results = []
    for i in range(0, len(messages), batch_size):
        batch = messages[i : i + batch_size]
        response = client.embeddings.create(
            model=model,
            input=batch,
        )
        for idx, data in enumerate(response.data):
            all_results.append(
                {
                    "text": batch[idx],
                    "embedding": data.embedding,
                    "model": model,
                    "dimensions": len(data.embedding),
                }
            )
    return all_results


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def find_similar_logs(
    query_message: str,
    candidate_messages: List[str],
    top_k: int = 5,
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
) -> List[Dict[str, Any]]:
    """
    Find the most semantically similar log messages to a query.

    Embeds the query and all candidates, then ranks by cosine similarity.

    Args:
        query_message: The query log message.
        candidate_messages: List of candidate log messages to search.
        top_k: Number of top similar results to return.
        client: Optional pre-configured OpenAI client.
        model: The OpenAI embedding model to use.

    Returns:
        List of similar messages with similarity scores, sorted descending.
    """
    if client is None:
        client = get_openai_client()

    # Embed query
    query_result = embed_log_message(query_message, client=client, model=model)
    query_vec = query_result["embedding"]

    # Embed candidates
    candidate_results = embed_log_messages(candidate_messages, client=client, model=model)

    # Compute similarities
    scored = []
    for candidate in candidate_results:
        score = cosine_similarity(query_vec, candidate["embedding"])
        scored.append(
            {
                "message": candidate["text"],
                "similarity": round(score, 4),
            }
        )

    # Sort by similarity descending
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def prepare_for_vector_store(
    messages: List[str],
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
    metadata_fields: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """
    Prepare log messages with embeddings for storage in a vector database.

    Generates embeddings and pairs them with optional metadata for
    ingestion into Pinecone, Weaviate, or similar vector stores.

    Args:
        messages: Log messages to prepare.
        client: Optional pre-configured OpenAI client.
        model: The OpenAI embedding model to use.
        metadata_fields: Optional list of metadata dicts to pair with each message.

    Returns:
        List of records with id, embedding, text, and metadata.
    """
    results = embed_log_messages(messages, client=client, model=model)

    records = []
    for idx, result in enumerate(results):
        record = {
            "id": f"log-{idx}",
            "values": result["embedding"],
            "metadata": {
                "text": result["text"],
                "model": result["model"],
                "dimensions": result["dimensions"],
            },
        }
        if metadata_fields and idx < len(metadata_fields):
            record["metadata"].update(metadata_fields[idx])
        records.append(record)

    return records


def main() -> None:
    """Example: embed log messages and find similar ones."""
    log_messages = [
        "Database connection timeout after 30 seconds on primary replica",
        "Failed to authenticate: API key expired for service account svc-payment",
        "HTTP 503 Service Unreturned from upstream load balancer",
        "Disk space critically low: /var/log partition at 97% capacity",
        "SSL certificate verification failed for api.external-provider.com",
        "Memory allocation failed: out of heap space for worker process 4",
    ]

    query = "Unable to connect to the database due to network timeout"

    similar = find_similar_logs(query, log_messages, top_k=3)

    print(f"Query: {query}")
    print(f"\nTop similar log messages:")
    for result in similar:
        print(f"  [{result['similarity']:.4f}] {result['message']}")

    print("\n\nFull embedding records for vector store:")
    records = prepare_for_vector_store(log_messages)
    for record in records:
        summary = {
            "id": record["id"],
            "text": record["metadata"]["text"],
            "dimensions": record["metadata"]["dimensions"],
        }
        print(json.dumps(summary))


if __name__ == "__main__":
    main()
