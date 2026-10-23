import os
from google.cloud import secretmanager
from vertexai.language_models import TextEmbeddingModel


def embed_secret_audit_notes(secret_name: str, project_id: str) -> list:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}"
    secret = client.get_secret(request={"name": name})
    text = f"{secret.name} {dict(secret.labels)} {getattr(secret, 'etag', '')}"
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embedding = model.get_embeddings([text])[0]
    return list(embedding.values)
