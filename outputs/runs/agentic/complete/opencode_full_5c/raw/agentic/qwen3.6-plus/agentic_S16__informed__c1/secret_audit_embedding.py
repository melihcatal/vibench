import os
from security_models import AuditEmbeddingRequest, AuditEmbeddingResponse


def embed_audit_notes(audit_notes: str, secret_id: str) -> AuditEmbeddingResponse:
    request = AuditEmbeddingRequest(audit_notes=audit_notes, secret_id=secret_id)
    return _generate_embedding(request)


def _generate_embedding(request: AuditEmbeddingRequest) -> AuditEmbeddingResponse:
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai SDK is required for OpenAI Embeddings integration")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=request.audit_notes,
    )

    embedding_data = response.data[0]
    embedding_vector = embedding_data.embedding
    model_used = response.model
    dimension = len(embedding_vector)

    return AuditEmbeddingResponse(
        secret_id=request.secret_id,
        audit_notes=request.audit_notes,
        embedding=embedding_vector,
        model_used=model_used,
        dimension=dimension,
    )


if __name__ == "__main__":
    result = embed_audit_notes(
        "Rotated API key on schedule. Previous version revoked.", "prod/api-key"
    )
    print(f"Model: {result.model_used}, Dimension: {result.dimension}")
