from google.cloud import aiplatform
from security_models import SecretAuditEmbedding


def embed_secret_audit_notes(
    secret_id: str, version_id: str, audit_text: str
) -> SecretAuditEmbedding:
    aiplatform.init(project="GOOGLE_CLOUD_PROJECT", location="us-central1")
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@latest")
    embeddings = model.get_embeddings([audit_text])

    return SecretAuditEmbedding(
        secret_id=secret_id,
        version_id=version_id,
        embedding=embeddings[0].values,
        audit_text=audit_text,
    )
