import os
import google.generativeai as genai


def embed_audit_notes(text: str) -> list[float]:
    """Embeds secret audit notes for semantic search using Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "embedding-001"
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
