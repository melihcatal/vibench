import google.generativeai as genai
import os

def get_gemini_embeddings_client():
    """Provides a configured Google Gemini Embeddings client."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai # The genai module itself acts as the client for embedding calls

EMBEDDING_MODEL_NAME = "models/embedding-001"

if __name__ == '__main__':
    try:
        client = get_gemini_embeddings_client()
        print("Google Gemini Embeddings client configured successfully.")
        # You can now use client.embed_content from other modules
    except ValueError as e:
        print(f"Error configuring client: {e}")
