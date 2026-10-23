import google.generativeai as genai
import os

def get_gemini_embeddings_client():
    """Configures and returns the Google Generative AI client for embeddings.

    Returns:
        A configured Google Generative AI client.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai

def get_embedding_model_name() -> str:
    """Returns the name of the embedding model to use.

    Returns:
        The embedding model name string.
    """
    return "models/embedding-001"
