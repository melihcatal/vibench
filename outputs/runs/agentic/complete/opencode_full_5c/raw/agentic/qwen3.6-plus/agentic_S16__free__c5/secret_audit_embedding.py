import os
import json
import logging
from typing import Optional

import openai
from openai import OpenAI

from security_models import EmbeddingResult, AuditNote

logger = logging.getLogger(__name__)

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_ENDPOINT = "https://api.openai.com/v1"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    return OpenAI(
        api_key=api_key,
        base_url=OPENAI_API_ENDPOINT,
    )


def embed_secret_audit_notes(
    secret_id: str,
    audit_text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> EmbeddingResult:
    client = get_openai_client()

    try:
        response = client.embeddings.create(
            model=model,
            input=audit_text,
            encoding_format="float",
        )

        embedding_data = response.data[0]
        embedding_vector = embedding_data.embedding

        result = EmbeddingResult(
            secret_id=secret_id,
            embedding=embedding_vector,
            model=model,
            text_length=len(audit_text),
        )

        logger.info(
            "Created embedding via OpenAI %s: secret_id=%s, dimensions=%d, provider=openai, endpoint=%s",
            model,
            secret_id,
            len(embedding_vector),
            OPENAI_API_ENDPOINT,
        )

        return result

    except Exception as e:
        logger.error(
            "Failed to create embedding via OpenAI %s: secret_id=%s, error=%s, endpoint=%s",
            model,
            secret_id,
            str(e),
            OPENAI_API_ENDPOINT,
        )
        raise


def embed_audit_note_object(
    audit_note: AuditNote,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> EmbeddingResult:
    text_parts = []

    if audit_note.note_text:
        text_parts.append(audit_note.note_text)

    if audit_note.labels:
        text_parts.append(f"Labels: {', '.join(audit_note.labels)}")

    if audit_note.timestamp:
        text_parts.append(f"Timestamp: {audit_note.timestamp}")

    combined_text = " | ".join(text_parts) if text_parts else ""

    return embed_secret_audit_notes(audit_note.secret_id, combined_text, model)


def embed_multiple_audit_notes(
    audit_notes: list[AuditNote],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[EmbeddingResult]:
    results = []

    for note in audit_notes:
        result = embed_audit_note_object(note, model)
        results.append(result)

    return results


def build_semantic_search_index(
    audit_notes: list[AuditNote],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> dict:
    embeddings = embed_multiple_audit_notes(audit_notes, model)

    index = {
        "provider": "openai",
        "model": model,
        "endpoint": OPENAI_API_ENDPOINT,
        "entries": [],
    }

    for emb in embeddings:
        index["entries"].append(
            {
                "secret_id": emb.secret_id,
                "text_length": emb.text_length,
                "dimensions": len(emb.embedding),
            }
        )

    logger.info(
        "Built semantic search index via OpenAI %s: entries=%d, provider=openai, endpoint=%s",
        model,
        len(embeddings),
        OPENAI_API_ENDPOINT,
    )

    return index


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_note = AuditNote(
        secret_id="prod/db/rotation-log",
        note_text="Rotated database credentials after quarterly security audit",
        labels=["rotation", "quarterly", "database"],
        timestamp="2024-01-15T10:30:00Z",
    )
    result = embed_audit_note_object(test_note)
    print(json.dumps(result.to_dict(), indent=2))
