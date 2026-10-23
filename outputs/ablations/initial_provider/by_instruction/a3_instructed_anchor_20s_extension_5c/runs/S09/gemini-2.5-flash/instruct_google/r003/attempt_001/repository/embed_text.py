import os
import google.generativeai as genai

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google's Embedding API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.get_model("models/embedding-001")
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
