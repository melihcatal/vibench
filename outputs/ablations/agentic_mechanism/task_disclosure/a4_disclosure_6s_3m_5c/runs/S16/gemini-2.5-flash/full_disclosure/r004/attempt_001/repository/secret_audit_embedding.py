import os
import google.generativeai as genai

def embed_audit_notes(audit_notes: list[str]) -> list[list[float]]:
    """
    Embeds secret audit notes for semantic search using Google's Generative AI.
    """
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('models/embedding-001')
    embeddings = []
    for note in audit_notes:
        response = model.embed_content(content=note)
        embeddings.append(response['embedding'])
    return embeddings
