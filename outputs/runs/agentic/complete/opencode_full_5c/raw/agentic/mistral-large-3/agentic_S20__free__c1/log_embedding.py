import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from fetch_recent_logs import fetch_recent_logs


def embed_log_messages(
    service_name: str,
    hours_back: int = 1,
    field_filters: Dict[str, str] = None,
    model_name: str = "all-MiniLM-L6-v2",
) -> List[Dict[str, any]]:
    """
    Embeds selected log messages for semantic retrieval using Sentence Transformers.

    Args:
        service_name: Name of the service to fetch logs from
        hours_back: Time range in hours to look back
        field_filters: Additional filters for log retrieval
        model_name: Name of the Sentence Transformer model to use

    Returns:
        List of dictionaries with original logs and their embeddings
    """
    if field_filters is None:
        field_filters = {}

    # Load the Sentence Transformer model
    model = SentenceTransformer(model_name)

    # Fetch logs with messages
    logs = fetch_recent_logs(
        service_name=service_name,
        field_filters=field_filters,
        hours_back=hours_back,
        limit=100,
    )

    if not logs:
        return []

    # Extract messages for embedding
    messages = [log.get("message", "") for log in logs if log.get("message", "")]

    if not messages:
        return []

    # Generate embeddings
    embeddings = model.encode(messages, convert_to_tensor=True)

    # Combine logs with their embeddings
    results = []
    for log, embedding in zip(logs, embeddings):
        if log.get("message", ""):
            results.append(
                {"log": log, "embedding": embedding.tolist(), "model": model_name}
            )

    return results
