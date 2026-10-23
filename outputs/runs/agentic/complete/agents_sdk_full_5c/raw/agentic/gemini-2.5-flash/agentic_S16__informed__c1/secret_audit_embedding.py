import google.generativeai as genai
import os

def embed_audit_notes(audit_notes: str) -> list[float]:
    """Embeds secret audit notes for semantic search using Google Gemini Embeddings."""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Using a specific embedding model from Gemini API
    model = "models/embedding-001"

    try:
        response = genai.embed_content(model=model, content=audit_notes)
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []

if __name__ == "__main__":
    # Set GOOGLE_API_KEY environment variable before running
    # For example: export GOOGLE_API_KEY="your-gemini-api-key"
    if "GOOGLE_API_KEY" not in os.environ:
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        example_audit_note = "Audit log entry for secret access. User 'admin' accessed 'db_password' at 2023-10-27 10:30:00 UTC."
        try:
            embedding = embed_audit_notes(example_audit_note)
            print(f"Embedding of audit note (first 5 elements): {embedding[:5]}...")
            print(f"Embedding dimension: {len(embedding)}")
        except Exception as e:
            print(f"Error creating audit note embedding: {e}")
