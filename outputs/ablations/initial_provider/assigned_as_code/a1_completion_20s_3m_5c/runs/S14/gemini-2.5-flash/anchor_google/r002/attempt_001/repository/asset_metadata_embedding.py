from typing import Optional

import vertexai
from vertexai.language_models import TextEmbeddingModel
from storage_models import AssetMetadataEmbeddingPayload, StorageConfig
import os

def asset_metadata_embedding(payload: AssetMetadataEmbeddingPayload, config: Optional[StorageConfig] = None) -> dict:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if config and config.project_id:
        project_id = config.project_id
    
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided in config or GOOGLE_CLOUD_PROJECT environment variable.")

    vertexai.init(project=project_id, location="us-central1") # Assuming us-central1 for Vertex AI
    model = TextEmbeddingModel.from_pretrained("text-embedding-004") # Using text-embedding-004 model

    content_to_embed = f"Object Name: {payload.object_name}"
    if payload.text_content:
        content_to_embed += f"\nContent: {payload.text_content}"

    embeddings = model.get_embeddings([content_to_embed])

    return {"embedding": embeddings[0].values}
