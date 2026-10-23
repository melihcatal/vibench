import os
import google.generativeai as genai

# GOOGLE_API_KEY environment variable should be set


def embed_caption_chunk(
    text_chunk: str, model_name: str = "models/embedding-001"
) -> list[float]:
    """Generates embeddings for a given text chunk using the Google Gemini Embeddings API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set.")
        return []

    genai.configure(api_key=api_key)

    try:
        response = genai.embed_content(model=model_name, content=text_chunk)
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []
