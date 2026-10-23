import os
import json
import requests
from security_models import AuditEmbedding


OPENAI_API_URL = "https://api.openai.com/v1/embeddings"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def embed_audit_notes(
    secret_id: str, audit_notes: str, model: str = None
) -> AuditEmbedding:
    model = model or DEFAULT_EMBEDDING_MODEL
    api_key = get_openai_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": audit_notes,
        "model": model,
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()

    embedding_data = result["data"][0]
    embedding_vector = embedding_data["embedding"]
    usage = result.get("usage", {})

    return AuditEmbedding(
        secret_id=secret_id,
        audit_notes=audit_notes,
        embedding=embedding_vector,
        model=model,
        dimension=len(embedding_vector),
    )


def embed_multiple_audit_notes(entries: list, model: str = None) -> list:
    model = model or DEFAULT_EMBEDDING_MODEL
    api_key = get_openai_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    texts = [e.get("audit_notes", "") for e in entries]

    payload = {
        "input": texts,
        "model": model,
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()

    embeddings = []
    for i, item in enumerate(result["data"]):
        entry = entries[i] if i < len(entries) else {}
        embeddings.append(
            AuditEmbedding(
                secret_id=entry.get("secret_id", f"entry-{i}"),
                audit_notes=entry.get("audit_notes", ""),
                embedding=item["embedding"],
                model=model,
                dimension=len(item["embedding"]),
            )
        )

    return embeddings


def build_audit_search_index(secret_audit_entries: list, model: str = None) -> dict:
    embeddings = embed_multiple_audit_notes(secret_audit_entries, model=model)
    index = {
        "model": model or DEFAULT_EMBEDDING_MODEL,
        "entries": [],
    }
    for emb in embeddings:
        index["entries"].append(
            {
                "secret_id": emb.secret_id,
                "dimension": emb.dimension,
                "embedding": emb.embedding,
            }
        )
    return index


if __name__ == "__main__":
    sample_secret_id = os.environ.get("AUDIT_SECRET_ID", "prod/api/payment-key")
    sample_notes = "Secret rotated on 2025-03-15. Previous version had exposure risk due to shared access. Rotation completed successfully via Lambda arn:aws:lambda:us-east-1:123456789:function:rotate-secrets."
    result = embed_audit_notes(sample_secret_id, sample_notes)
    print(f"Model: {result.model}, Dimension: {result.dimension}")
