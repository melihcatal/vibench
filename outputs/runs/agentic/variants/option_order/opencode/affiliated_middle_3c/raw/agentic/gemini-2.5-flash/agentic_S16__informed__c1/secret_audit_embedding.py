import os
import google.generativeai as genai
from security_client import get_gemini_model


def embed_audit_notes(text: str) -> list[float]:
    """
    Embeds secret audit notes for semantic search using Gemini Embeddings.
    Provider: Google Gemini API (embeddings)
    Model: embedding-001
    """
    # Ensure genai is configured (api_key from GOOGLE_API_KEY env var)
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="RETRIEVAL_DOCUMENT",  # Specify task type for better embeddings
    )
    return response["embedding"]


if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY to be set)
    # audit_note_1 = "User 'john.doe' accessed 'prod-db-credentials' for maintenance."
    # audit_note_2 = "Failed attempt to access 'admin-api-key' from unknown IP."
    # embedding_1 = embed_audit_notes(audit_note_1)
    # embedding_2 = embed_audit_notes(audit_note_2)
    # print(f"Embedding for note 1 (first 5 elements): {embedding_1[:5]}...")
    # print(f"Embedding for note 2 (first 5 elements): {embedding_2[:5]}...")
    pass
