import cohere
import os


def embed_secret_audit_notes(audit_notes: str) -> list:
    """
    Embeds secret audit notes for semantic search using Cohere's embeddings API.
    
    Args:
        audit_notes: The audit notes to embed.
        
    Returns:
        A list of embeddings as floats.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=[audit_notes],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings[0]