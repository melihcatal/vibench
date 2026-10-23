import os
import google.generativeai as genai

# Specify the concrete model identifier or model family
EMBEDDING_MODEL_NAME = "models/text-embedding-004" # Or "models/embedding-001" depending on availability/preference

def configure_gemini_api():
    """
    Configures the Gemini API client with the API key from environment variables.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

def get_embeddings_model():
    """
    Returns an initialized Gemini embeddings model client.
    """
    configure_gemini_api()
    return genai.GenerativeModel(EMBEDDING_MODEL_NAME)

if __name__ == "__main__":
    # Example usage:
    # Set your GOOGLE_API_KEY environment variable before running.
    # For instance: export GOOGLE_API_KEY='your_api_key_here'
    try:
        model = get_embeddings_model()
        print(f"Successfully initialized Gemini embeddings model: {EMBEDDING_MODEL_NAME}")
    except ValueError as e:
        print(f"Error initializing model: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
