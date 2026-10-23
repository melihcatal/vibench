import os
from google.cloud import genai

def embed_script(text: str) -> list[float]:
    """Create a text embedding for a narration script using Google Gemini embeddings.

    Returns the embedding vector as a list of floats.
    Requires GOOGLE_API_KEY environment variable.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    embedding = model.embed_content(text)
    return embedding.embedding_data.vector