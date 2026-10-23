import google.generativeai as genai
import os


def embed_crypto_audit_note(
    audit_note: str, model_name: str = "models/embedding-001"
) -> list[float]:
    """Generates an embedding for a crypto audit note using Google Gemini Embeddings."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    try:
        response = genai.embed_content(
            model=model_name, content=audit_note, task_type="RETRIEVAL_DOCUMENT"
        )
        return response["embedding"]
    except Exception as e:
        raise RuntimeError(f"Error generating embedding: {e}")
