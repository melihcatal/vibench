from typing import List
from security_client import get_cohere_client

def embed_audit_notes(notes: List[str], model: str = "embed-english-v3.0"):
    """
    Creates vector embeddings for crypto audit notes for semantic search.
    Uses the Cohere Embed API.
    """
    cohere_client = get_cohere_client()

    if not notes:
        return {"embeddings": [], "error": "No notes provided."}

    try:
        response = cohere_client.embed(
            texts=notes,
            model=model,
            input_type="search_document" # or "search_query"
        )
        return {
            "embeddings": response.embeddings,
            "model_used": model
        }
    except Exception as e:
        return {"embeddings": [], "error": str(e)}
