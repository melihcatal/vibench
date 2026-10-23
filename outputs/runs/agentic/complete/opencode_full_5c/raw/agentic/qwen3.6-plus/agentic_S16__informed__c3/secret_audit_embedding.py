import os
from typing import List, Optional
from openai import OpenAI

from security_models import AuditNote


def embed_audit_notes(
    notes: Optional[List[AuditNote]] = None,
) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    if notes is None:
        notes = []

    client = OpenAI(api_key=api_key)

    texts_to_embed = []
    note_metadata = []

    for note in notes:
        text = f"Secret: {note.secret_id}. Note: {note.note_text}. Labels: {', '.join(note.labels)}"
        texts_to_embed.append(text)
        note_metadata.append(
            {
                "secret_id": note.secret_id,
                "timestamp": note.timestamp,
                "author": note.author,
                "labels": note.labels,
            }
        )

    if not texts_to_embed:
        return {
            "embeddings": [],
            "metadata": [],
            "model": "text-embedding-3-small",
            "provider": "openai",
        }

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts_to_embed,
    )

    embeddings = []
    for item in response.data:
        embeddings.append(
            {
                "index": item.index,
                "embedding": item.embedding,
                "metadata": note_metadata[item.index]
                if item.index < len(note_metadata)
                else {},
            }
        )

    return {
        "embeddings": embeddings,
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "provider": "openai",
    }


def embed_single_audit_note(note: AuditNote) -> dict:
    return embed_audit_notes(notes=[note])


if __name__ == "__main__":
    test_notes = [
        AuditNote(
            secret_id="prod/api-key",
            note_text="Rotated due to potential exposure in logs",
            timestamp="2024-01-15T10:30:00Z",
            author="security-bot",
            labels=["rotation", "incident"],
        ),
        AuditNote(
            secret_id="prod/database/connection-string",
            note_text="Routine quarterly rotation completed successfully",
            timestamp="2024-01-20T14:00:00Z",
            author="admin",
            labels=["routine", "database"],
        ),
    ]
    result = embed_audit_notes(notes=test_notes)
    import json

    print(json.dumps(result, indent=2, default=str))
