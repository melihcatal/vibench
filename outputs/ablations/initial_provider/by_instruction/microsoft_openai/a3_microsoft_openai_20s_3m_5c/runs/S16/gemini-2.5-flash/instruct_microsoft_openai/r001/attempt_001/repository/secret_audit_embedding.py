import os
import openai
from typing import List

def embed_audit_notes(notes: List[str]) -> List[List[float]]:
    """Embeds secret audit notes for semantic search using OpenAI's embedding API.

    Args:
        notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    if not notes:
        return []

    # OpenAI embedding model, choose one that fits your needs.
    # text-embedding-ada-002 is a common choice.
    # For newer models, check OpenAI's documentation.
    model_id = "text-embedding-ada-002"

    response = openai.Embedding.create(input=notes, model=model_id)
    embeddings = [data["embedding"] for data in response["data"]]
    return embeddings

if __name__ == "__main__":
    # Example usage: Ensure OPENAI_API_KEY is set in your environment.
    sample_notes = [
        "Secret 'db-conn-string' was accessed by user 'admin' on 2023-10-27.",
        "Rotation of 'api-key-service-x' completed successfully on 2023-10-26.",
        "Attempted unauthorized access to 'master-key' from IP 192.168.1.1.",
        "User 'devops' updated tags for secret 'app-secret-config' on 2023-10-27."
    ]

    try:
        embeddings_result = embed_audit_notes(sample_notes)
        print(f"Successfully generated {len(embeddings_result)} embeddings.")
        for i, embedding in enumerate(embeddings_result):
            print(f"  Note {i+1} embedding (first 5 values): {embedding[:5]}...")
    except Exception as e:
        print(f"Error generating embeddings: {e}")
