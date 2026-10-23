import os
import google.generativeai as genai

def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using Google Gemini Embeddings.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    try:
        response = genai.get_embedding(
            model="models/embedding-001",
            content=text
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

