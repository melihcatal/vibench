import os
from google.cloud import aiplatform
from google.cloud.aiplatform.models import TextEmbeddingModel

def platform_output_embedding(text_to_embed: str) -> list[float]:
    """
    Embed platform outputs for evaluation or retrieval using Google Vertex AI.

    Args:
        text_to_embed: The text content to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")

    aiplatform.init(project=project_id, location=location)

    # Use a provider-specific model identifier from Vertex AI Model Garden
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    embeddings = model.get_embeddings([text_to_embed])
    
    return embeddings[0].values
