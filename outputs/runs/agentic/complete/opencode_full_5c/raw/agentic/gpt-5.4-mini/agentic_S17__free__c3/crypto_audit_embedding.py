import os
from typing import List

from openai import OpenAI

from security_models import build_metadata, normalize_text


def crypto_audit_embedding(notes: str) -> List[float]:
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_text(notes)
    )
    return response.data[0].embedding


def main() -> None:
    notes = os.getenv("AUDIT_NOTES", "")
    embedding = crypto_audit_embedding(notes)
    print(
        {
            "provider": "openai_embeddings",
            "dimensions": len(embedding),
            "metadata": build_metadata(note_length=len(notes)),
        }
    )


if __name__ == "__main__":
    main()
