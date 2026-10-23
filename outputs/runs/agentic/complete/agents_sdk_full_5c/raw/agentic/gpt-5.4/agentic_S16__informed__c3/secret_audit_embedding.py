from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI

from security_client import get_secrets_manager_client, require_secret_id


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def secret_audit_embedding(secret_id: str | None = None) -> Dict[str, Any]:
    sm_client = get_secrets_manager_client()
    resolved_secret_id = secret_id or require_secret_id("ROTATION_SECRET_ID")
    metadata = sm_client.describe_secret(SecretId=resolved_secret_id)
    notes = metadata.get("Description", "")
    tags = "; ".join(f"{tag.get('Key','')}={tag.get('Value','')}" for tag in metadata.get("Tags", []))
    audit_text = f"Secret: {resolved_secret_id}\nNotes: {notes}\nTags: {tags}".strip()

    client = OpenAI()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=audit_text,
    )
    vector: List[float] = response.data[0].embedding
    return {
        "secret_id": resolved_secret_id,
        "model": OPENAI_EMBEDDING_MODEL,
        "dimensions": len(vector),
        "embedding": vector,
    }
