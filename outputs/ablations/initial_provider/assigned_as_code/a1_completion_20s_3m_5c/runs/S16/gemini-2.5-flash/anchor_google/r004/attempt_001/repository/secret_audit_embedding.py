from security_client import get_embedding_model
from security_models import AuditEmbedding
from typing import List

def embed_secret_audit_notes(secret_id: str, notes: str):
    model = get_embedding_model()
    embeddings = model.get_embeddings([notes])
    embedding_vector = [embedding.values for embedding in embeddings][0]

    return AuditEmbedding(
        secret_id=secret_id,
        notes=notes,
        embedding_vector=embedding_vector
    ).__dict__
