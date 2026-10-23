import os
from security_client import get_gemini_client
import google.generativeai as genai # Provider-identifying signal

def embed_audit_notes(audit_note: str) -> list[float]:
    """
    Embeds secret audit notes for semantic search using Gemini Embeddings.
    """
    genai_client = get_gemini_client()
    
    try:
        response = genai_client.embed_content(
            model="models/embedding-001", # Concrete model identifier
            content=audit_note
        )
        return response['embedding']
    except Exception as e:
        raise RuntimeError(f"Failed to embed audit notes with Gemini Embeddings API: {e}")
