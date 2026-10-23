"""
Embeds crypto audit notes for semantic search using Cohere.
"""
import os
import cohere
from typing import List

def embed_audit_notes(notes: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of crypto audit notes using the Cohere API.

    Args:
        notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embedding vectors, one for each note.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=notes,
            model='embed-english-v3.0',
            input_type='search_document'
        )
        return response.embeddings
    except cohere.core.api_error.ApiError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []

# Example Usage (for demonstration if run directly)
if __name__ == '__main__':
    audit_log_notes = [
        "User 'alice' successfully decrypted configuration file 'prod-db.conf' with key 'alias/prod-config'.",
        "Key 'alias/testing-key' was used for a signing operation by service account 'ci-runner'.",
        "Decryption failed for user 'bob' attempting to access 'archive.zip' with key 'alias/prod-config'. Check permissions.",
        "Scheduled key rotation initiated for 'alias/prod-config'. New version created.",
    ]

    if os.environ.get("COHERE_API_KEY"):
        print("Embedding audit notes...")
        embeddings = embed_audit_notes(audit_log_notes)
        if embeddings:
            print(f"Successfully generated {len(embeddings)} embeddings.")
            print(f"Dimension of first embedding: {len(embeddings[0])}")
            # print("First embedding (first 5 dimensions):", embeddings[0][:5])
    else:
        print("Skipping example: COHERE_API_KEY environment variable not set.")
