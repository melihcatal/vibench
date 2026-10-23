import google.generativeai as genai
import os

def embed_audit_note(audit_note_text: str) -> list[float]:
    """
    Generates an embedding for crypto audit notes using Google Gemini Embeddings.

    Args:
        audit_note_text: The text of the crypto audit note.

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    model = 'models/embedding-001' # Specific model for embeddings
    response = genai.embed_content(
        model=model,
        content=audit_note_text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']
