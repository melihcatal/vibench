from google.cloud import secretmanager
from vertexai.language_models import TextEmbeddingModel


def secret_audit_embedding(payload, config=None):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{payload['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    text = payload.get("notes") or secret.name
    embedding = model.get_embeddings([text])[0].values
    return {"embedding": embedding}
