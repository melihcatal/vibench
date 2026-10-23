from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_client import load_security_client_config

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_secret_audit_notes(notes: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = "\n".join(notes)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    print(embed_secret_audit_notes(["rotation completed", "no unsafe access detected"]))
