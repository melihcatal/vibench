import os
from google.cloud import aiplatform


def embed_moderation_rationale(text: str) -> list[float]:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv(
        "GOOGLE_CLOUD_LOCATION", "us-central1"
    )  # PaLM embeddings are regional
    model_name = "text-embedding-004"  # A common text embedding model

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    embeddings = model.predict([text])

    if embeddings and embeddings.embeddings:
        return embeddings.embeddings[0].values
    return []
