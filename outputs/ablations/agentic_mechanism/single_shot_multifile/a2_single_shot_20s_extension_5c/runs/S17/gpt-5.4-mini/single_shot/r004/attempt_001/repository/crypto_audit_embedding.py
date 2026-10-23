from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI


def embed_crypto_audit_notes(notes: List[str]) -> Dict[str, Any]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=notes)
    return {"provider": "openai", "model": "text-embedding-3-small", "embeddings": [item.embedding for item in response.data]}


def main() -> Dict[str, Any]:
    notes = [line for line in os.environ.get("AUDIT_NOTES", "").split("\n") if line]
    return embed_crypto_audit_notes(notes)
