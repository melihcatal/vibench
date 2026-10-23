import os
import json
import openai
from security_client import describe_secret, get_secrets_manager_client
from security_models import AuditEmbedding


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.environ.get(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)


client = openai.OpenAI(api_key=OPENAI_API_KEY)


def embed_audit_text(text: str, model: str = None) -> AuditEmbedding:
    target_model = model or OPENAI_EMBEDDING_MODEL
    response = client.embeddings.create(
        model=target_model,
        input=text,
    )
    embedding_data = response.data[0]
    return AuditEmbedding(
        secret_id="",
        audit_text=text,
        embedding=embedding_data.embedding,
        model_used=target_model,
        dimension=len(embedding_data.embedding),
    )


def embed_secret_audit_notes(
    secret_id: str = None, notes: str = None
) -> AuditEmbedding:
    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    metadata = describe_secret(target_id)
    if notes is None:
        notes = metadata.get("Description", "")
        tags = metadata.get("Tags", [])
        tag_text = ", ".join(f"{t.get('Key')}={t.get('Value')}" for t in tags)
        if tag_text:
            notes = f"{notes}. Tags: {tag_text}"
    embedding = embed_audit_text(notes)
    embedding.secret_id = target_id
    return embedding


def embed_multiple_audit_notes(entries: list) -> list:
    texts = [e.get("text", "") for e in entries if e.get("text")]
    if not texts:
        return []
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=texts,
    )
    results = []
    for i, data in enumerate(response.data):
        entry = entries[i] if i < len(entries) else {}
        results.append(
            AuditEmbedding(
                secret_id=entry.get("secret_id", ""),
                audit_text=texts[i],
                embedding=data.embedding,
                model_used=OPENAI_EMBEDDING_MODEL,
                dimension=len(data.embedding),
            )
        )
    return results


def build_audit_search_index(secret_ids: list = None) -> list:
    if secret_ids is None:
        env_val = os.environ.get("SECRET_IDS_LIST", "")
        secret_ids = [s.strip() for s in env_val.split(",") if s.strip()]
    embeddings = []
    for sid in secret_ids:
        try:
            emb = embed_secret_audit_notes(secret_id=sid)
            embeddings.append(emb)
        except Exception as e:
            embeddings.append(
                AuditEmbedding(
                    secret_id=sid,
                    audit_text=f"Error: {str(e)}",
                    embedding=[],
                    model_used=OPENAI_EMBEDDING_MODEL,
                )
            )
    return embeddings


def cosine_similarity(vec_a: list, vec_b: list) -> float:
    import math

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def search_similar_audit_notes(query_text: str, index: list, top_k: int = 5) -> list:
    query_embedding = embed_audit_text(query_text)
    scored = []
    for entry in index:
        if entry.embedding:
            score = cosine_similarity(query_embedding.embedding, entry.embedding)
            scored.append(
                {
                    "secret_id": entry.secret_id,
                    "audit_text": entry.audit_text,
                    "similarity": score,
                }
            )
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    emb = embed_secret_audit_notes()
    print(f"Secret: {emb.secret_id}")
    print(f"Model: {emb.model_used}")
    print(f"Dimension: {emb.dimension}")
    print(f"Embedding preview: {emb.embedding[:5]}...")
