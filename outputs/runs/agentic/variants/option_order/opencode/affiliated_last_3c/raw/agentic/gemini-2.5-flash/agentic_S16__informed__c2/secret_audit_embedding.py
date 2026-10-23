import os
from openai import OpenAI


def embed_secret_audit_notes(text: str) -> list[float]:
    """Embeds secret audit notes for semantic search using OpenAI Embeddings."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=[text],
            model="text-embedding-ada-002",  # Concrete model identifier
        )
        return response.data[0].embedding
    except Exception as e:
        raise Exception(f"Error creating embedding: {e}")
