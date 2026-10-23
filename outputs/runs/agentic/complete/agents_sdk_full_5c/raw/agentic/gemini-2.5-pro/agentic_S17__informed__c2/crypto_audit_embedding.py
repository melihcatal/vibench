import os
import cohere
from typing import List

def embed_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    """
    Embeds cryptographic audit notes for semantic search using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=audit_notes,
            model='embed-english-v3.0',
            input_type='search_document'
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []
