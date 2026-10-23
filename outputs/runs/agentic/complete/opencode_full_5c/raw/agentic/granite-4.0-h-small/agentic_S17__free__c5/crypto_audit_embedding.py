# [LATER-STEP] crypto_audit_embedding.py
import json
from openai import OpenAI

# Embed crypto audit notes for downstream semantic search


def embed_audit_note(note: str) -> dict:
    """Sends a free‑form audit note to an LLM to obtain an embedding vector.

    Returns the embedding ID and vector (as a list of floats).
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embedding = client.embeddings.create(
        model="text-embedding-ada-002",
        input=note,
    )
    return {
        "note": note,
        "embedding_id": embedding.data[0].embedding_id,
        "vector": embedding.data[0].embedding,
        "provider": "openai",
    }
