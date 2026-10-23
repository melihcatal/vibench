import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def moderation_reason_embedding(reasons: List[str], config: Dict[str, Any] = None) -> List[List[float]]:
    config = config or {}

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", config.get("google_cloud_project"))
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", config.get("google_cloud_location", "us-central1"))

    if not project_id:
        raise ValueError("Google Cloud Project ID not provided. Set GOOGLE_CLOUD_PROJECT env var or pass in config.")

    aiplatform.init(project=project_id, location=location)

    # Use the TextEmbeddingModel for embeddings
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

    embeddings = model.predict(reasons)
    return [embedding.values for embedding in embeddings]
