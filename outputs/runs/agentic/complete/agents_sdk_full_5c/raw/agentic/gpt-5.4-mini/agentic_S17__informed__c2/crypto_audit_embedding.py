from __future__ import annotations

from openai import OpenAI

from security_models import normalize_text_payload

EMBED_MODEL = "text-embedding-3-small"


def embed_crypto_audit_notes(notes: str) -> list[float]:
    client = OpenAI()
    text = normalize_text_payload(notes)
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding


if __name__ == "__main__":
    pass
