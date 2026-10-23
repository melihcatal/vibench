import openai
import os
from typing import List

def embed_audit_notes(notes: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using OpenAI Embeddings.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    try:
        response = openai.Embedding.create(
            input=notes,
            model=model
        )
        return [embedding.embedding for embedding in response['data']]
    except Exception as e:
        raise RuntimeError(f"Failed to embed audit notes with OpenAI: {e}")

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY environment variable)
    # Set OPENAI_API_KEY before running
    # audit_notes = [
    #     "Secret 'db-conn' accessed by user 'admin' for daily report.",
    #     "Rotation initiated for 'api-key-service-x' due to policy violation."
    # ]
    # embeddings = embed_audit_notes(audit_notes)
    # for i, emb in enumerate(embeddings):
    #     print(f"Embedding for note {i+1}: {emb[:5]}...") # Print first 5 dimensions
    pass
