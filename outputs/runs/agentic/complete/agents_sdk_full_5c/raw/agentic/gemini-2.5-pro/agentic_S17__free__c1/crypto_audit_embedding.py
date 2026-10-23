
import os
import cohere
from typing import List

def embed_crypto_audit_notes(notes: List[str]) -> List[List[float]]:
    """
    Embeds cryptocurrency audit notes for semantic search using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        # Using a specific, high-performance model from Cohere
        response = co.embed(
            texts=notes,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return []

