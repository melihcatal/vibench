from typing import Dict, List
import os
import numpy as np

from observability_client import get_logging_client
from sentence_transformers import SentenceTransformer


def embed_log_messages(
    log_messages: List[str],
    model_name: str = "all-MiniLM-L6-v2",
) -> List[Dict[str, any]]:
    """
    Embeds selected log messages for semantic retrieval using Sentence Transformers.

    Args:
        log_messages: A list of log messages to embed.
        model_name: The Sentence Transformer model to use for embedding.

    Returns:
        A list of dictionaries containing the original message and its embedding.
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(log_messages, convert_to_numpy=True)

    results = []
    for message, embedding in zip(log_messages, embeddings):
        results.append(
            {
                "message": message,
                "embedding": embedding.tolist(),
            }
        )

    return results


def fetch_logs_for_embedding(
    service: str,
    limit: int = 50,
) -> List[str]:
    """
    Fetches logs from Datadog for embedding.

    Args:
        service: The service to fetch logs for.
        limit: Maximum number of logs to fetch.

    Returns:
        A list of log messages.
    """
    client = get_logging_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    query = f"service:{service}"
    results = client.query(
        query=query,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    return [log.get("message", "") for log in results]


if __name__ == "__main__":
    log_messages = fetch_logs_for_embedding(service="search-service", limit=20)
    embedded_results = embed_log_messages(log_messages)
    print(f"Generated {len(embedded_results)} embeddings")
