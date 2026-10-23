import google.generativeai as genai
import os

def embed_caption_chunk(caption_chunk: str) -> list[float]:
    """Embeds caption chunks for semantic meeting search using Gemini Embeddings."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    response = genai.embed_content(
        model=model,
        content=caption_chunk,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']
