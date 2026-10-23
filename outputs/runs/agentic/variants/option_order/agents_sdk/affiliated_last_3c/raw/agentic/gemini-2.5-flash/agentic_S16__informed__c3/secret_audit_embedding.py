import os
import openai
from typing import List

def embed_audit_notes(text_notes: List[str]) -> List[List[float]]:
    """Embeds secret audit notes for semantic search using OpenAI Embeddings.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        client = openai.OpenAI(api_key=openai.api_key)
        # Using the recommended embedding model text-embedding-ada-002
        # as of OpenAI's documentation.
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text_notes
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings with OpenAI: {e}")

