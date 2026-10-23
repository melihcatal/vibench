import os
import json
from observability_models import LogEvent
from google.cloud import (
    aiplatform,
)  # concrete provider SDK for Vertex AI / Gemini embeddings


def log_embedding(log_event: LogEvent) -> dict:
    """Embed selected log messages for semantic retrieval using Gemini Embeddings.

    Returns a dictionary containing the embedding vector and metadata.
    """
    # Authenticate using GOOGLE_APPLICATION_CREDENTIALS environment variable
    embed_client = aiplatform.Embeddings(model="models/embed-text-001")

    text = log_event.message
    response = embed_client.embed_content(text)
    embedding = response.embedding.values  # list of floats
    metadata = {
        "id": log_event.correlationId or str(hash(log_event.message))[:8],
        "timestamp": str(log_event.timestamp),
        "severity": log_event.severity,
    }
    return {"embedding": embedding, "metadata": metadata}
