import os
import google.generativeai as genai

# Configure the Gemini API with the API key from environment variables
# GOOGLE_API_KEY is the provider-specific environment variable.
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def get_gemini_model(model_name: str):
    """
    Provides a configured Google Gemini GenerativeModel instance.
    """
    return genai.GenerativeModel(model_name)

def get_gemini_embedder(model_name: str):
    """
    Provides a configured Google Gemini embedding model instance.
    """
    return genai.get_model(model_name) # Embeddings use get_model
