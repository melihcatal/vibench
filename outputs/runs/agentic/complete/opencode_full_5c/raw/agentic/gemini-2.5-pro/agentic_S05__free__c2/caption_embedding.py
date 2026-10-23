import os
import google.generativeai as genai


def embed_caption_chunk(caption_chunk: str):
    """Embeds a caption chunk for semantic meeting search."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable must be set.")
    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    result = genai.embed_content(
        model=model, content=caption_chunk, task_type="retrieval_document"
    )

    return result["embedding"]
