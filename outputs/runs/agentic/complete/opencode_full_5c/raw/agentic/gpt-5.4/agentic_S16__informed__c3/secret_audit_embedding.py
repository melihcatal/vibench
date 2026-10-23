from __future__ import annotations

from security_client import embed_text
from security_models import AuditEmbedding, normalize_embedding


def secret_audit_embedding(audit_note: str) -> dict:
    result = embed_text(audit_note)
    embedding = result["embedding"]
    payload = AuditEmbedding(
        text=audit_note,
        vector=embedding,
        model=result["model"],
        dimensions=len(embedding),
    )
    return normalize_embedding(payload)
