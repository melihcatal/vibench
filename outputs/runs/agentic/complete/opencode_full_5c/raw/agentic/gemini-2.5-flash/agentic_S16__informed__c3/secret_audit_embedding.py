import os
import google.generativeai as genai
from security_client import get_gemini_embedding_model


def embed_secret_audit_notes(notes: list[str]) -> list[list[float]]:
    """Embeds secret audit notes for semantic search using Google Gemini Embeddings.

    Args:
        notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embedding vectors, one for each note.
    """
    model = get_gemini_embedding_model(
        "embedding-001"
    )  # Using 'embedding-001' as the concrete model identifier
    try:
        # The embedding model expects a list of texts for batch embedding
        result = model.embed_content(contents=notes)
        # Extract the embedding vectors from the response
        return [embedding.values for embedding in result.embeddings]
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings with Gemini API: {e}")
