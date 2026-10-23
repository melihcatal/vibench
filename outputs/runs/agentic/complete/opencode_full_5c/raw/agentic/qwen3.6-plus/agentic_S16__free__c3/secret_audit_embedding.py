from typing import Optional
import os
import requests

from security_models import AuditEmbedding
from security_client import get_vault_client


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_audit_notes(
    secret_path: str,
    audit_text: Optional[str] = None,
    mount_point: Optional[str] = None,
) -> AuditEmbedding:
    if audit_text is None:
        client = get_vault_client()
        try:
            response = client.read_secret(
                client._build_secret_url(secret_path, mount_point).split("/data/")[-1]
            )
            audit_text = response.metadata.get("audit_notes", "")
        finally:
            client.close()

    if not audit_text:
        audit_text = f"Audit notes for secret at path: {secret_path}"

    api_key = os.environ.get("OPENAI_API_KEY", "")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_EMBEDDING_MODEL,
        "input": audit_text,
        "encoding_format": "float",
    }

    resp = requests.post(
        OPENAI_EMBEDDINGS_URL, json=payload, headers=headers, timeout=30
    )
    resp.raise_for_status()
    result = resp.json()

    data = result.get("data", [])
    if not data:
        raise ValueError("No embedding data returned from OpenAI API")

    embedding_data = data[0]
    embedding = embedding_data.get("embedding", [])
    dimensions = len(embedding)

    return AuditEmbedding(
        secret_path=secret_path,
        audit_text=audit_text,
        embedding=embedding,
        model=OPENAI_EMBEDDING_MODEL,
        dimensions=dimensions,
    )


def embed_multiple_audit_notes(
    secret_paths: list[str], mount_point: Optional[str] = None
) -> list[AuditEmbedding]:
    results = []
    for path in secret_paths:
        embedding = embed_audit_notes(path, mount_point=mount_point)
        results.append(embedding)
    return results


if __name__ == "__main__":
    import os

    secret_path = os.environ.get("AUDIT_SECRET_PATH", "prod/database/postgres-primary")
    result = embed_audit_notes(secret_path)
    print(result.to_dict())
