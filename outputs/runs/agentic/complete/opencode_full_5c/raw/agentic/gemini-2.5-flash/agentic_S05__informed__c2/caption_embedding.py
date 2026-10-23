import os
import google.generativeai as genai


def embed_caption_chunk(text: str) -> list[float]:
    """
    Embeds a caption chunk for semantic meeting search using Google Gemini Embeddings.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Provider-identifying signal: google.generativeai and model ID
    result = genai.embed_content(
        model="models/embedding-001", content=text, task_type="RETRIEVAL_DOCUMENT"
    )

    return result["embedding"]
