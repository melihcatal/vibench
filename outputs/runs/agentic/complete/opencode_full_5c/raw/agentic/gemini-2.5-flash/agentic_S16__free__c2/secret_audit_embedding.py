import os
from typing import List
from google.cloud import aiplatform


def secret_audit_embedding(
    text_notes: List[str], project_id: str = None, location: str = "us-central1"
) -> List[List[float]]:
    project_id = project_id if project_id else os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError(
            "GCP_PROJECT_ID environment variable or project_id must be set."
        )

    aiplatform.init(project=project_id, location=location)

    # Using the TextEmbeddingModel from Vertex AI for embeddings
    # Model ID: text-embedding-004
    # Note: This model is subject to change and may incur costs.
    model = aiplatform.preview.language_models.TextEmbeddingModel.from_pretrained(
        "text-embedding-004"
    )
    embeddings = model.get_embeddings(text_notes)

    return [embedding.values for embedding in embeddings]
