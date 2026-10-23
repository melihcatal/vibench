import os
from openai import OpenAI


def embed_audit_notes(audit_notes: str) -> list[float]:
    """
    Embeds secret audit notes for semantic search using OpenAI Embeddings.
    Requires OPENAI_API_KEY environment variable to be set.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=audit_notes,
            model="text-embedding-ada-002",  # or another suitable OpenAI embedding model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error creating embedding with OpenAI API: {e}")
        raise
