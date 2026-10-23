import google.generativeai as genai
import os

def embed_audit_notes(audit_note: str) -> list[float]:
    """
    Embeds secret audit notes for semantic search using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model_name = "models/embedding-001" # Using a concrete model identifier

    try:
        response = genai.embed_content(
            model=model_name,
            content=audit_note
        )
        return response['embedding']
    except Exception as e:
        print(f"Error embedding audit note with Google Gemini API: {e}")
        raise

