import google.generativeai as genai  # Provider SDK import
import os


def embed_caption_chunk(text_chunk: str):
    """Embeds a caption chunk for semantic meeting search using Google Generative AI (Gemini/PaLM API)."""
    # Ensure GOOGLE_API_KEY is set in environment variables
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable not set."

    # Using an embedding model, e.g., text-embedding-004 (example model ID)
    model = "models/embedding-001"  # Provider-specific model ID/family

    try:
        result = genai.embed_content(model=model, content=text_chunk)
        return result["embedding"]
    except Exception as e:
        return f"Error embedding caption: {e}"
