import os

from google.cloud import aiplatform
from vertexai.preview.language_models import TextEmbeddingModel


def embed_caption_chunk(caption_chunk: str) -> list[float]:
    """Embeds a caption chunk for semantic meeting search using Google Cloud Vertex AI Text Embedding."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set for Vertex AI."
        )

    # Initialize Vertex AI
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)

    model = TextEmbeddingModel.from_pretrained(
        "textembedding-gecko@001"
    )  # Using textembedding-gecko for embeddings

    try:
        embeddings = model.get_embeddings([caption_chunk])
        return embeddings[0].values
    except Exception as e:
        print(f"Error during embedding generation: {str(e)}")
        return []
