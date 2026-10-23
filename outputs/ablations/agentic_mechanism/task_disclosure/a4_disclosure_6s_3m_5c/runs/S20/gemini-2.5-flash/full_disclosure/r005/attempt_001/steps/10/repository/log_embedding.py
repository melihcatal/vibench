from typing import List
from google.cloud import aiplatform

def embed_log_messages(project_id: str, location: str, log_messages: List[str]) -> List[List[float]]:
    """
    Embeds selected log messages using Google Cloud Vertex AI's TextEmbeddingModel.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        log_messages: A list of log messages to embed.

    Returns:
        A list of embedding vectors, where each vector corresponds to a log message.
    """
    aiplatform.init(project=project_id, location=location)

    # The TextEmbeddingModel can be initialized with a specific model ID.
    # "text-embedding-004" is a commonly used model for text embeddings.
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings(log_messages)
    return [embedding.values for embedding in embeddings]

