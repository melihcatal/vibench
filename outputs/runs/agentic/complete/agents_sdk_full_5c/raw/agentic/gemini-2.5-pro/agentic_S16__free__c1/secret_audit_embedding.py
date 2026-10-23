import os
from openai import OpenAI
from typing import List

def embed_secret_audit_embedding(note_text: str) -> List[float]:
    """
    Embeds secret audit notes for semantic search using OpenAI's embedding models.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=note_text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error calling OpenAI embeddings API: {e}")
        raise

