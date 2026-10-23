import os
import google.generativeai as genai


def configure_gemini_client():
    """
    Configures the Google Generative AI client with the API key from environment variables.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)


def get_gemini_embedding_model_name() -> str:
    """
    Returns the default Gemini embedding model name.
    """
    return "models/embedding-001"
