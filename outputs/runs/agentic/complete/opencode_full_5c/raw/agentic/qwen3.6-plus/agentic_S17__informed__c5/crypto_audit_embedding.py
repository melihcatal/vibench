from openai import OpenAI
from security_models import (
    AuditEmbeddingRequest,
    AuditEmbeddingResponse,
    AuditEmbeddingResult,
)
from security_client import load_openai_config


def embed_audit_notes(request: AuditEmbeddingRequest) -> AuditEmbeddingResponse:
    config = load_openai_config()

    api_key = config["api_key"]
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")

    client = OpenAI(api_key=api_key, base_url=config["base_url"])

    model = request.model or "text-embedding-3-small"

    response = client.embeddings.create(
        input=request.audit_notes,
        model=model,
    )

    embeddings = []
    total_tokens = 0

    for idx, embedding_data in enumerate(response.data):
        embeddings.append(
            AuditEmbeddingResult(
                text=request.audit_notes[idx],
                embedding=embedding_data.embedding,
                index=idx,
            )
        )
        total_tokens += embedding_data.get("usage", {}).get("total_tokens", 0)

    if total_tokens == 0 and hasattr(response, "usage"):
        total_tokens = response.usage.total_tokens

    return AuditEmbeddingResponse(
        embeddings=embeddings,
        model=model,
        total_tokens=total_tokens,
        request_id=response.id or "",
        metadata={
            "provider": "openai",
            "model_id": model,
            "num_notes": len(request.audit_notes),
        },
    )
