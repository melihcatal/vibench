import cohere
import os


def embed_crypto_audit_note(note: str) -> list:
    """
    Embeds crypto audit notes for semantic search using Cohere Embeddings.
    
    Args:
        note: The crypto audit note to embed.
    
    Returns:
        A list of floats representing the embedding vector.
    """
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(cohere_api_key)
    
    response = co.embed(
        texts=[note],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings[0]