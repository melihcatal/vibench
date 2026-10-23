import json
import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def _chunk_notes(notes: Iterable[str]) -> List[str]:
    return [note.strip() for note in notes if note and note.strip()]


def embed_crypto_audit_notes(notes: Iterable[str]) -> list:
    items = _chunk_notes(notes)
    if not items:
        return []
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=items)
    return [datum.embedding for datum in response.data]


def embed_notes_from_json(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    notes = payload if isinstance(payload, list) else payload.get("notes", [])
    vectors = embed_crypto_audit_notes(notes)
    return json.dumps({"model": OPENAI_EMBEDDING_MODEL, "vectors": vectors})


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("usage: python crypto_audit_embedding.py <notes.json>")
    print(embed_notes_from_json(sys.argv[1]))
