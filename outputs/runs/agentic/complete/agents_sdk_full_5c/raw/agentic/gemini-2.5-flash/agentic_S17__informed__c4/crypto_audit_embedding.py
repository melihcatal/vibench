import google.generativeai as genai
import os

def embed_audit_note(audit_note: str) -> list[float]:
    """
    Embeds crypto audit notes for semantic search using Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = 'embedding-001'

    response = genai.embed_content(
        model=model,
        content=audit_note,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']

