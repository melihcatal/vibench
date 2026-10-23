import os
import openai
from typing import List

def embed_audit_notes(text: str) -> List[float]:
    """Embeds secret audit notes for semantic search using OpenAI Embeddings.

    Args:
        text (str): The audit note text to embed.

    Returns:
        List[float]: A list of floats representing the embedding vector.
    """
    # Ensure OPENAI_API_KEY environment variable is set
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    # Using a concrete model identifier
    embedding_model = "text-embedding-ada-002"

    try:
        response = openai.embeddings.create(input=[text], model=embedding_model)
        # The response structure is .data[0].embedding for the first (and only) input text
        return response.data[0].embedding
    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error during embedding: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during embedding: {e}")

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY env var)
    # audit_note_1 = "User 'jdoe' accessed 'db-prod-password' on 2023-10-27 for emergency access."
    # embedding_1 = embed_audit_notes(audit_note_1)
    # print(f"Embedding for note 1 (first 5 elements): {embedding_1[:5]}...")

    # audit_note_2 = "'api-service-account' rotated 'stripe-api-key' successfully on 2023-10-27."
    # embedding_2 = embed_audit_notes(audit_note_2)
    # print(f"Embedding for note 2 (first 5 elements): {embedding_2[:5]}...")
    pass
