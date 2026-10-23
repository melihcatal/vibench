import os
import google.generativeai as genai

def embed_asset_metadata_and_text(text: str) -> list[float]:
    # Google Cloud Generative AI setup
    # Ensure GOOGLE_API_KEY is set in environment variables
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel('embedding-001') # Using embedding-001 for embeddings
    response = model.embed_content(content=text)
    return response['embedding']
