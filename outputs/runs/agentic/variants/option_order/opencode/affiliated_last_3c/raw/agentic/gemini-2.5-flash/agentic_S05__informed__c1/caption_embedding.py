import os
import google.generativeai as genai

# GOOGLE_API_KEY environment variable should be set
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def embed_caption_chunk(caption_chunk: str) -> list[float]:
    """Embeds caption chunks for semantic meeting search using Google Gemini Embeddings."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    model = genai.GenerativeModel("embedding-001")  # Using embedding-001 for embeddings

    response = model.embed_content(content=caption_chunk)
    return response["embedding"]
