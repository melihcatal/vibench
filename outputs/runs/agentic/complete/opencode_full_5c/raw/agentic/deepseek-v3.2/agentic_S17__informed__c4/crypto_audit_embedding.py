import os
from typing import List
from security_models import EmbeddingResult
import openai


def embed_crypto_audit_notes(audit_notes: str) -> EmbeddingResult:
    """
    Embed crypto audit notes for semantic search using OpenAI embeddings.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return EmbeddingResult(
            success=False,
            error="OPENAI_API_KEY environment variable is required",
            provider="openai",
        )

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=audit_notes, encoding_format="float"
        )

        embedding = response.data[0].embedding

        return EmbeddingResult(success=True, embedding=embedding, provider="openai")

    except Exception as e:
        return EmbeddingResult(success=False, error=str(e), provider="openai")
