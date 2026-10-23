import cohere
import os


def embed_secret_audit_notes(text: str) -> list:
    """
    Embed secret audit notes for semantic search using Cohere Embed API.
    
    Args:
        text: The audit notes to embed.
    
    Returns:
        A list of embeddings (floats).
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=[text], model="embed-english-v3.0")
    return response.embeddings[0]