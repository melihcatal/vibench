from google.cloud import secretmanager

from vertexai.language_models import TextEmbeddingModel


def secret_audit_embedding(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    text = payload.get("notes") or (secret.annotations or {}).get("audit_notes", "")
    embedding = model.get_embeddings([text])[0].values
    return {"embedding": embedding}
