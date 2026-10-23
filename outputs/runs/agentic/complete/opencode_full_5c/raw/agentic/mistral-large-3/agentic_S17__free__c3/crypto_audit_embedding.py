from typing import Dict, Any
import os
from openai import OpenAI


def embed_crypto_audit_note(note: str) -> Dict[str, Any]:
    """Embeds crypto audit notes for semantic search using OpenAI text-embedding-3-small."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(input=note, model="text-embedding-3-small")

    return {
        "embedding": response.data[0].embedding,
        "model": "text-embedding-3-small",
        "usage": response.usage.model_dump(),
    }
