import os
from typing import Optional
from openai import OpenAI
from security_models import AuditNote, EmbeddingResult


OPENAI_MODEL = "text-embedding-3-small"


def embed_audit_note(
    note: AuditNote,
    model: str = OPENAI_MODEL,
) -> EmbeddingResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model=model,
        input=note.note_text,
        encoding_format="float",
    )
    embedding = response.data[0].embedding
    return EmbeddingResult(
        text=note.note_text,
        embedding=embedding,
        model=model,
        secret_name=note.secret_name,
    )


def embed_audit_notes(
    notes: list[AuditNote],
    model: str = OPENAI_MODEL,
) -> list[EmbeddingResult]:
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    texts = [note.note_text for note in notes]
    response = client.embeddings.create(
        model=model,
        input=texts,
        encoding_format="float",
    )
    results = []
    for i, data in enumerate(response.data):
        results.append(
            EmbeddingResult(
                text=notes[i].note_text,
                embedding=data.embedding,
                model=model,
                secret_name=notes[i].secret_name,
            )
        )
    return results


def embed_audit_text(
    text: str,
    secret_name: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> EmbeddingResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float",
    )
    embedding = response.data[0].embedding
    return EmbeddingResult(
        text=text,
        embedding=embedding,
        model=model,
        secret_name=secret_name,
    )


def compute_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)
