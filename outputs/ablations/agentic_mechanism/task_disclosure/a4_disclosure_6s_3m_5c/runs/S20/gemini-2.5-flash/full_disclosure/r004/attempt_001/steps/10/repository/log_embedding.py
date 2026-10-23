from google.cloud import aiplatform

def embed_log_messages(project_id: str, location: str, log_messages: list[str]) -> list[list[float]]:
    """
    Embeds selected log messages using Google Cloud Vertex AI's TextEmbeddingModel.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        log_messages: A list of log messages to embed.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)

    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-gecko@001")
    embeddings = model.get_embeddings(log_messages)

    return [embedding.values for embedding in embeddings]
