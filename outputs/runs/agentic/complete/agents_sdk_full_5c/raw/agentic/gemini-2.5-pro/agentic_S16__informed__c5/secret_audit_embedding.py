"""Embed secret audit notes for semantic search using Cohere."""
import os
import cohere
from typing import List, Optional

def embed_audit_notes(notes: List[str]) -> Optional[List[List[float]]]:
    """
    Generates embeddings for a list of secret audit notes using Cohere.

    Args:
        notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embeddings, where each embedding is a list of floats, or None on error.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=notes,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.core.api_error.ApiError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None

if __name__ == '__main__':
    audit_notes_to_embed = [
        "User 'admin' successfully rotated the secret 'prod/db/main' on 2023-10-27.",
        "Access denied for user 'guest' attempting to read secret 'prod/db/main'.",
        "Secret 'staging/api/payment' rotation failed due to invalid credentials test.",
        "Scheduled rotation for 'prod/billing-api' completed without errors.",
    ]
    
    embeddings = embed_audit_notes(audit_notes_to_embed)
    
    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        print("Embedding dimension:", len(embeddings[0]))
        # print("First embedding (truncated):", embeddings[0][:5])
    else:
        print("Failed to generate embeddings.")
