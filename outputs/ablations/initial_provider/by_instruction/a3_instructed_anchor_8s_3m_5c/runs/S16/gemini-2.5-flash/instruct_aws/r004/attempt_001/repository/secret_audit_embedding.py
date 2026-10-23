import os
from typing import List

import cohere

def embed_audit_notes(notes: List[str]) -> List[List[float]]:
    co = cohere.Client(os.environ.get("COHERE_API_KEY")) # This is your trial API key
    try:
        response = co.embed(
            texts=notes,
            model="embed-english-light-v3.0", # Use a suitable embedding model
            input_type="search_document"
        )
        return response.embeddings
    except Exception as e:
        print(f"Error generating embeddings with Cohere: {e}")
        return []

if __name__ == '__main__':
    # Example usage (requires COHERE_API_KEY environment variable)
    audit_notes_examples = [
        "Secret 'db_password_prod' was accessed by user 'admin' for maintenance on 2026-09-18.",
        "Rotation of 'api_key_dev' completed successfully. New version staged.",
        "Failed attempt to access 'root_ssh_key' from unauthorized IP 192.168.1.100.",
        "User 'devops' updated labels for 'external_service_token' to include 'compliance:pci'."
    ]

    embeddings = embed_audit_notes(audit_notes_examples)

    if embeddings:
        print(f"Generated {len(embeddings)} embeddings. First embedding (first 5 values): {embeddings[0][:5]}...")
        # In a real application, you would store these embeddings in a vector database
        # for semantic search.
        # For example, to find similar audit notes:
        # query_embedding = embed_audit_notes(["Failed login attempts to production database"])[0]
        # Perform similarity search with query_embedding against stored embeddings.
    else:
        print("Failed to generate embeddings.")
