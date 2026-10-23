from __future__ import annotations

import os
from typing import List

from openai import OpenAI


EMBED_MODEL = "text-embedding-3-small"


def embed_audit_notes(notes: str) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.embeddings.create(model=EMBED_MODEL, input=notes)
    return list(result.data[0].embedding)


def main() -> List[float]:
    notes = os.environ.get("AUDIT_NOTES", "Secret access reviewed and approved.")
    return embed_audit_notes(notes)


if __name__ == "__main__":
    print(main())
