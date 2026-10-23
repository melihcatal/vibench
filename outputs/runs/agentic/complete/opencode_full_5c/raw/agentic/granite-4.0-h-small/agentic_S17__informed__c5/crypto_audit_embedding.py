# crypto_audit_embedding.py
# Embed crypto audit notes for semantic search / downstream retrieval

import os
import openai
from datetime import datetime

# Provider: OpenAI embeddings (or Azure OpenAI, both use openai SDK)
# Expected env vars: OPENAI_API_KEY (or AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

openai.api_key = OPENAI_API_KEY

# Model to use: text-embedding-ada-002 (default for OpenAI)
embedding_model = "text-embedding-ada-002"


def embed_audit_note(note: str) -> str:
    """Generate an embedding (base64 string) for the supplied audit note.","""
    response = openai.Embedding.create(
        model=embedding_model,
        input=note,
    )
    embedding = response["data"][0]["embedding"]
    # Return as a JSON‑serializable list of floats
    return str(embedding)


if __name__ == "__main__":
    note = "User encrypted a financial record using key 'data-encrypt-key-v1'. No unsafe content detected."
    embedding = embed_audit_note(note)
    print("Embedding bytes (base64):", embedding)
