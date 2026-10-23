from typing import List

from google.cloud import secretmanager
from vertexai.language_models import TextEmbeddingModel

from security_client import load_config


def secret_audit_embedding(notes: List[str]):
    config = load_config()
    secretmanager.SecretManagerServiceClient()
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(notes)
    return {"project_id": config.project_id, "embeddings": [embedding.values for embedding in embeddings]}
