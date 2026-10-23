import google.generativeai as genai
import os

def embed_audit_notes(text: str) -> list[float]:
    """Embeds secret audit notes for semantic search using Gemini Embeddings."
    # GOOGLE_API_KEY environment variable is used for authentication
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    response = genai.embed_content(model_name="models/embedding-001", content=text)
    return response['embedding']
