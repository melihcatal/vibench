import os
from openai import OpenAI


def crypto_audit_embedding(audit_notes: str, api_key: str = None) -> dict:
    """
    Embeds crypto audit notes for semantic search using OpenAI embeddings.

    Args:
        audit_notes: The crypto audit notes to embed.
        api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.

    Returns:
        Dictionary containing embedding, model, provider, and success status.
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "error": "OpenAI API key not provided",
            "provider": "openai",
            "success": False,
        }

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=audit_notes, model="text-embedding-ada-002"
        )

        return {
            "embedding": response.data[0].embedding,
            "model": "text-embedding-ada-002",
            "provider": "openai",
            "success": True,
        }
    except Exception as e:
        return {"error": str(e), "provider": "openai", "success": False}
