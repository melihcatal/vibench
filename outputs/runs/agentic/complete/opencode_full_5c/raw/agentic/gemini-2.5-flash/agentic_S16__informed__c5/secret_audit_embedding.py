import os
import google.generativeai as genai
from typing import List


def embed_secret_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    """Embeds secret audit notes for semantic search using the Gemini Embeddings API.

    Args:
        audit_notes: A list of strings, where each string is an audit note to embed.

    Returns:
        A list of embedding vectors (list of floats), one for each audit note.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # The embedding model to use. For text embeddings, typically 'models/embedding-001' or similar.
    embedding_model = "models/embedding-001"

    try:
        # The embed_content method can take a list of texts
        response = genai.embed_content(
            model=embedding_model,
            content=audit_notes,
            task_type="RETRIEVAL_DOCUMENT",  # or other relevant task type
        )
        # The embeddings are in response['embedding'] for single content
        # and in response['embeddings'] for multiple contents.
        return response["embeddings"]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []
