import os
from google.cloud import aiplatform


def embed_text_for_translation_memory(text: str) -> list[float]:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # The model ID for text embeddings on Vertex AI is 'text-embedding-004'
    # or similar, depending on the version.
    # Using the TextEmbeddingModel.from_pretrained method for pre-trained models.
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    # Predict embeddings
    embeddings = model.get_embeddings([text])[0].values

    return embeddings
