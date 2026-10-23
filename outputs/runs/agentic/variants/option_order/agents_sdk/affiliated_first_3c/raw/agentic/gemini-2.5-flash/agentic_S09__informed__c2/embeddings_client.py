import os
import google.generativeai as genai

def get_gemini_embeddings_client():
    """Configures and returns the Google Gemini Embeddings client."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    # The embedding model is used directly in the embed_content calls
    # This function primarily ensures the API key is configured.
    return genai # Return the configured genai module itself for direct use

EMBEDDING_MODEL_NAME = "models/embedding-001"

if __name__ == '__main__':
    # Example usage (ensure GOOGLE_API_KEY is set)
    # from dotenv import load_dotenv
    # load_dotenv()
    # try:
    #     client = get_gemini_embeddings_client()
    #     print("Gemini Embeddings client configured successfully.")
    #     # You can now use client.embed_content(...)
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
