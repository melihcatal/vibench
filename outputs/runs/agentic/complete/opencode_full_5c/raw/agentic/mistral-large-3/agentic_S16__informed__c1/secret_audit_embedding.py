from typing import List, Dict, Optional
import os
import cohere
from numpy import array, ndarray


def embed_secret_audit_notes(audit_notes: List[str]) -> Optional[Dict[str, ndarray]]:
    """
    Embeds secret audit notes for semantic search using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Cohere API key not configured.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=audit_notes, model="embed-english-v3.0", input_type="search_document"
        )

        return {
            "embeddings": array(response.embeddings),
            "texts": audit_notes,
            "model": response.model,
        }
    except Exception as e:
        print(f"Failed to embed audit notes: {e}")
        return None
