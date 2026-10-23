import os
from security_models import EmbeddingResult
from security_client import create_openai_embedding

OPENAI_EMBEDDING_MODEL = os.environ.get(
    "AUDIT_EMBEDDING_MODEL", "text-embedding-3-small"
)
DEFAULT_DIMENSIONS = int(os.environ.get("EMBEDDING_DIMENSIONS", "256"))


def embed_audit_note(
    secret_name: str,
    audit_note: str,
    model: str = None,
    dimensions: int = None,
) -> EmbeddingResult:
    target_model = model or OPENAI_EMBEDDING_MODEL
    target_dims = dimensions or DEFAULT_DIMENSIONS

    embedding_vector = create_openai_embedding(
        text=audit_note,
        model=target_model,
        dimensions=target_dims,
    )

    return EmbeddingResult(
        secret_name=secret_name,
        audit_note=audit_note,
        embedding=embedding_vector,
        model=target_model,
        dimensions=len(embedding_vector),
    )


def embed_multiple_audit_notes(
    notes: list,
    model: str = None,
    dimensions: int = None,
) -> list:
    results = []
    for note in notes:
        secret_name = note.get("secret_name", "")
        audit_text = note.get("audit_note", "")
        result = embed_audit_note(secret_name, audit_text, model, dimensions)
        results.append(result)
    return results


def compute_embedding_similarity(vec_a: list, vec_b: list) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Embedding vectors must have the same dimension")
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)
