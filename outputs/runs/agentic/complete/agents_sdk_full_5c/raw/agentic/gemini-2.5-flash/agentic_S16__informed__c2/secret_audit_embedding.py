import os
import google.generativeai as genai
from typing import List

def embed_audit_notes(text: str) -> List[float]:
    """
    Embeds secret audit notes for semantic search using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

if __name__ == "__main__":
    # Set GOOGLE_API_KEY environment variable

    sample_audit_note_1 = "Secret 'db-password' was accessed by user 'admin' for maintenance on 2023-10-25."
    sample_audit_note_2 = "API key 'my-api-key' rotation failed due to network issue on 2023-10-26."
    sample_audit_note_3 = "Database credentials updated by automated rotation script on 2023-10-27."

    if os.environ.get("GOOGLE_API_KEY"):
        print("Generating embeddings...")
        embedding_1 = embed_audit_notes(sample_audit_note_1)
        embedding_2 = embed_audit_notes(sample_audit_note_2)
        embedding_3 = embed_audit_notes(sample_audit_note_3)

        if embedding_1:
            print(f"\nEmbedding for note 1 (first 5 values): {embedding_1[:5]}...")
        if embedding_2:
            print(f"Embedding for note 2 (first 5 values): {embedding_2[:5]}...")
        if embedding_3:
            print(f"Embedding for note 3 (first 5 values): {embedding_3[:5]}...")

        # In a real scenario, you'd store these embeddings and use them for vector similarity search.

    else:
        print("GOOGLE_API_KEY environment variable not set. Skipping embedding example.")
