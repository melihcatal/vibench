import os
import google.generativeai as genai


def get_gemini_client():
    """Initializes and returns a Google Gemini client for embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai


def get_embedding_model(client):
    """Returns the embedding model from the Gemini client."""
    return client.get_model("embedding-001")
