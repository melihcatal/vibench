import os
from openai import OpenAI
from security_models import EmbeddingResult


def embed_audit_note(note: str) -> EmbeddingResult:
    """Embeds secret audit notes for semantic search using OpenAI Embeddings.

    Args:
        note: The audit note text to embed.

    Returns:
        An EmbeddingResult object containing the embedding vector.

    Raises:
        Exception: If the OPENAI_API_KEY is not set or API call fails.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=note,
            model="text-embedding-ada-002",  # Or "text-embedding-3-small" as per reference
        )
        return EmbeddingResult(embedding=response.data[0].embedding)
    except Exception as e:
        raise Exception(f"OpenAI Embeddings API call failed: {e}")
