import os
import google.generativeai as genai
from embeddings_client import get_embeddings_model

def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using the Gemini embeddings model.
    """
    model = get_embeddings_model()
    response = model.embed_content(content=[text])
    # The Gemini API returns a list of embeddings, even for single content
    return response.embeddings[0].values

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set in your environment
    sample_text = "The quick brown fox jumps over the lazy dog."
    embedding = embed_text(sample_text)
    print(f"Embedding for \"{sample_text}\" (first 5 dimensions): {embedding[:5]}...")
    print(f"Embedding dimension: {len(embedding)}")
