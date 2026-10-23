import os
import google.generativeai as genai


def embed_caption_chunk(text_chunk: str) -> list[float]:
    """Generates embeddings for a text chunk using the Gemini Embeddings API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # The embedding model for text
    model = "models/embedding-001"

    response = genai.embed_content(
        model=model, content=text_chunk, task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]
