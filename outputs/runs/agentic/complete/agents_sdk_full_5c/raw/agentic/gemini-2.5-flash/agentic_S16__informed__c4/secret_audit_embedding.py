import google.generativeai as genai
import os

def embed_audit_note(audit_note_text: str) -> list[float] | None:
    """
    Generates an embedding for a secret audit note using the Google Gemini Embeddings API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY environment variable not set.")
        return None

    genai.configure(api_key=api_key)
    # Using the embedding-001 model for embeddings
    model_name = "embedding-001"

    try:
        response = genai.embed_content(
            model=model_name,
            content=audit_note_text,
            task_type="RETRIEVAL_DOCUMENT" # Suitable for semantic search
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return None
