import os
import google.generativeai as genai

EMBEDDING_MODEL = "models/embedding-001"


def get_gemini_client():
    """Configures and returns the Google Gemini client for embeddings."""
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    return genai


def get_embedding_model_name():
    """Returns the name of the embedding model."""
    return EMBEDDING_MODEL
