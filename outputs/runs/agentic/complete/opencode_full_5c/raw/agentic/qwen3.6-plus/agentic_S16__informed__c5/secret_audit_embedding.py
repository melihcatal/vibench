import os
from typing import Optional
from openai import OpenAI
from security_models import AuditNote


def embed_audit_notes(
    notes: list,
    model: str = "text-embedding-3-small",
    api_key: str = None,
) -> list:
    client = OpenAI(api_key=api_key or os.environ["OPENAI_API_KEY"])
    texts = []
    for note in notes:
        if isinstance(note, AuditNote):
            texts.append(note.note_text)
        elif isinstance(note, str):
            texts.append(note)
        elif isinstance(note, dict):
            texts.append(note.get("text", note.get("note_text", "")))
    response = client.embeddings.create(
        model=model,
        input=texts,
    )
    embeddings = [item.embedding for item in response.data]
    return embeddings


def create_audit_note_with_embedding(
    secret_id: str,
    note_text: str,
    timestamp: str = None,
    author: str = None,
    model: str = "text-embedding-3-small",
    api_key: str = None,
) -> AuditNote:
    client = OpenAI(api_key=api_key or os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model=model,
        input=note_text,
    )
    embedding = response.data[0].embedding
    return AuditNote(
        secret_id=secret_id,
        note_text=note_text,
        timestamp=timestamp,
        author=author,
        embedding=embedding,
    )


def embed_audit_notes_batch(
    audit_notes: list,
    model: str = "text-embedding-3-small",
    api_key: str = None,
) -> list:
    enriched_notes = []
    texts = []
    for note in audit_notes:
        if isinstance(note, AuditNote):
            texts.append(note.note_text)
        elif isinstance(note, str):
            texts.append(note)
        elif isinstance(note, dict):
            texts.append(note.get("text", note.get("note_text", "")))
    embeddings = embed_audit_notes(texts, model, api_key)
    for i, note in enumerate(audit_notes):
        if isinstance(note, AuditNote):
            note.embedding = embeddings[i]
            enriched_notes.append(note)
        elif isinstance(note, str):
            enriched_notes.append(
                AuditNote(
                    secret_id="",
                    note_text=note,
                    embedding=embeddings[i],
                )
            )
        elif isinstance(note, dict):
            enriched_notes.append(
                AuditNote(
                    secret_id=note.get("secret_id", ""),
                    note_text=note.get("text", note.get("note_text", "")),
                    timestamp=note.get("timestamp"),
                    author=note.get("author"),
                    embedding=embeddings[i],
                )
            )
    return enriched_notes


def compute_similarity(embedding_a: list, embedding_b: list) -> float:
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    sample_notes = [
        "Rotated production DB password after quarterly compliance review",
        "Updated API key following suspected exposure in logs",
        "Emergency rotation due to compromised service account",
    ]
    results = embed_audit_notes(sample_notes)
    print(f"Generated {len(results)} embeddings")
    print(f"Embedding dimension: {len(results[0])}")
