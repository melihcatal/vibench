import os
import google.generativeai as genai

# Configure the Gemini API client
# Ensure GOOGLE_API_KEY environment variable is set
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

def embed_caption_chunk(caption_chunk: str) -> list[float]:
    """Generates an embedding for a caption chunk using the Gemini Embeddings API (embedding-001 model)."""
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=caption_chunk,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []
