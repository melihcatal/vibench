import os
import google.generativeai as genai

def get_gemini_embeddings_client():
    """Configures and returns a Google Gemini Embeddings client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("embedding-001")

def get_gemini_llm_client():
    """Configures and returns a Google Gemini LLM client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-pro")
