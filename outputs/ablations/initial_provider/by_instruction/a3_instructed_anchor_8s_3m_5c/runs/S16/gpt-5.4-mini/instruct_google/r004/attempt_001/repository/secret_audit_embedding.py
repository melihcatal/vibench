from google.cloud import secretmanager
from vertexai.language_models import TextEmbeddingModel

from security_client import build_client, load_config, secret_payload_text, secret_version_path


def secret_audit_embedding(secret_id: str = "audit-secret", version_id: str = "latest"):
    config = load_config(secret_id, version_id)
    client: secretmanager.SecretManagerServiceClient = build_client()
    response = client.access_secret_version(request={"name": secret_version_path(config)})
    note = secret_payload_text(response)
    model = TextEmbeddingModel.from_pretrained("text-embedding-005")
    return model.get_embeddings([note])[0].values
